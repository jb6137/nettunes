from django.contrib.auth.models import User
from django.db import models
import datetime


class Record(models.Model):
    name = models.CharField(max_length=40, unique=True)
    num_owned = models.IntegerField()
    num_available = models.IntegerField()

    def __str__(self):
        return self.name

    def issue(self):
        self.num_available -= 1
        self.save()

    def turn_in(self):
        self.num_available += 1
        self.save()


class Rental(models.Model):
    customer = models.ForeignKey(User, related_name='rental', on_delete=models.CASCADE)
    record = models.ForeignKey(Record, related_name='rental', on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True)

    def close_out(self):
        self.returned_at = datetime.datetime.now()
        self.save()


class Request(models.Model):
    customer = models.ForeignKey(User, related_name='request', on_delete=models.CASCADE)
    record = models.ForeignKey(Record, related_name='request', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    rented_at = models.DateTimeField(null=True)
    order = models.IntegerField(null=True)

    def fulfill(self):
        self.rented_at = datetime.datetime.now()
        self.order = None
        self.save()

    def reorder(self, new_order):
        if new_order < 1:
            print(f"Error. Trying to set order to {new_order}. Order should run from 1.")
        self.order = new_order
        self.save()
        