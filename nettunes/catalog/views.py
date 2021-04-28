from catalog.models import Record, Rental, Request
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render


def about(request):
    return render(request, 'about.html')

def catalog(request):
    records = Record.objects.all()
    return render(request, 'catalog.html', {'records': records})

def account(request, username):
    user = User.objects.get(id=request.user.id)
    if username != user.username:
        return redirect('unauthorized')
    else:
        rentals = Rental.objects.filter(customer=user).exclude(returned_at__isnull=False)
        requests = Request.objects.filter(customer=user).exclude(rented_at__isnull=False)
        return render(request, 'account.html', {'username': username,'rentals': rentals, 'requests': requests})

def unauthorized(request):
    return HttpResponse("You are not authorized to do that.")

def login(Request):
    return render(request, 'login.html')

def request_record(request):
    if request.method == "POST":
        record_id = request.POST.get('id')
        record = Record.objects.get(id=record_id)
        user = User.objects.get(id=request.user.id)
        handle_record_request(user, record)
    return redirect('catalog')

def handle_record_request(user, record):
    if record_available(record) and not has_rented_max(user) and not is_rented(user, record):
        rent_record(user, record)
    else:
        user_queue = Request.objects.filter(customer=user).exclude(rented_at__isnull=False)
        if not is_on_queue(user_queue, record):
            queue_len = 0 if not user_queue else len(user_queue)
            queue_request(user, record, queue_len + 1) # we want order to start from 1. 
        else: # can't rent, nor put on queue
            # for now just print to terminal, instead of logging. TODO: add logging system.
            print(f"User {user.username} cannot rent nor put on queue record {record.name}")

def record_available(record):
    return record.num_available > 0

def has_rented_max(user):
    active_user_rentals = Rental.objects.filter(customer=user).exclude(returned_at__isnull=False)
    return len(active_user_rentals) >= 3

def is_rented(user, record):
    same_record_rented = Rental.objects.filter(customer=user, record=record).exclude(returned_at__isnull=False)
    return True if same_record_rented else False

def is_on_queue(user_queue, record):
    if not user_queue:
        return False

    same_record_on_queue = user_queue.filter(record=record)
    return True if same_record_on_queue else False

@transaction.atomic
def rent_record(user, record):
    rental = Rental(customer = user, record = record)
    record.issue()
    rental.save()

def queue_request(user, record, order):
    request = Request(customer=user, record=record, order=order)
    request.save()

@transaction.atomic
def return_rental(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        rental_id = request.POST.get('id')
        rental = Rental.objects.get(id=rental_id)
        if rental.customer != user:
            return redirect('unauthorized')
        record_id = rental.record_id
        record = Record.objects.get(id=record_id)
        record.turn_in()
        rental.close_out()
        if has_queue(user):
            rent_from_queue(user)
    return redirect('/')

def has_queue(user):
    queue = Request.objects.filter(customer=user).exclude(rented_at__isnull=False)
    return True if queue else False

def rent_from_queue(user):
    queue = get_sorted_user_queue(user)
    for record_request in queue:
        if has_rented_max(user):
            return
        record = record_request.record
        if record_available(record) and not is_rented(user, record):
            request_order = record_request.order
            fulfill_request(record_request)
            reorder_queue_after_removed_item(queue, request_order)

def get_sorted_user_queue(user):
    return Request.objects.filter(customer=user).exclude(rented_at__isnull=False).order_by('order')

@transaction.atomic
def fulfill_request(record_request):
    record = record_request.record
    request_order = record_request.order
    user = record_request.customer
    rent_record(user, record)
    record_request.fulfill()

@transaction.atomic
def reorder_queue_after_removed_item(user_queue, removed_item):
    """ Changes the order of the requests in the user_queue, starting with removed_item + 1.
        It is assumed that the request with order=removed_item has been deleted, or rented (at which point its
        order should have been set to None).
        Starting with order=removed_item + 1, subtracts 1 from the order. So n + 1=>n, n+2=>n+1, etc
        Note this expects user_queue to be sorted by order
    """
    for record_request in user_queue:
        if record_request.order and record_request.order > removed_item:
            record_request.reorder(record_request.order - 1)

def move_request_up(request):
    if request.method == "POST":
        request_id = request.POST.get('id')
        rental_request = Request.objects.get(id=request_id)
        user = request.user

        if rental_request.customer != user:
            print(f"Log: Request from {user.username} to move up a request belonging to {rental_request.customer.username}.")
            return redirect('unauthorized')

        request_order = rental_request.order
        if request_order > 1:
            queue = get_sorted_user_queue(user)
            swap_request_order(queue, request_order, request_order - 1)
    return redirect('/')

@transaction.atomic
def cancel_request(request):
    if request.method == "POST":
        request_id = request.POST.get('id')
        rental_request = Request.objects.get(id=request_id)
        user = request.user

        if rental_request.customer != user:
            print(f"Log: Request from {user.username} to cancel a request belonging to {rental_request.customer.username}.")
            return redirect('unauthorized')

        request_order = rental_request.order
        rental_request.delete()  
        
        queue = get_sorted_user_queue(user)
        reorder_queue_after_removed_item(queue, request_order)
    return redirect('/')

@transaction.atomic
def swap_request_order(queue, first_request_order, second_request_order):
    first_request = queue.get(order = first_request_order)
    second_request = queue.get(order = second_request_order)
    first_request.reorder(second_request_order)
    second_request.reorder(first_request_order)
