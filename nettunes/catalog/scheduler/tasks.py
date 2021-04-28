from catalog.models import Record, Rental, Request
from catalog.views import rent_from_queue
from django.utils import timezone
from datetime import timedelta


def fill_requests():
    print("Filling daily requests....")
    active_requests = Request.objects.exclude(rented_at__isnull=False).order_by('order', 'requested_at')
    user_list = [request.customer for request in active_requests]
    for user in user_list:
        rent_from_queue(user)

def generate_report():
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    daily_rentals = Rental.objects.filter(rented_at__gte=yesterday, rented_at__lte=now)
    print(f"Rentals from {yesterday} to {now}.")
    for rental in daily_rentals:
        print(f"Name: {rental.record.name} Customer: {rental.customer.username} time: {rental.rented_at}")