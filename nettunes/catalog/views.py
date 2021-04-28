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
