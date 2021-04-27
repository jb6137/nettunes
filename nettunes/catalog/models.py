from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=40, unique=True)
    num_owned = models.IntegerField()
    num_available = models.IntegerField()

    def __str__(self):
        return self.name


class Rental(models.Model):
    customer = models.ForeignKey(User, related_name='rental', on_delete=models.CASCADE)
    record = models.ForeignKey(Record, related_name='rental', on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True)


class Request(models.Model):
    customer = models.ForeignKey(User, related_name='request', on_delete=models.CASCADE)
    record = models.ForeignKey(Record, related_name='request', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    rented_at = models.DateTimeField(null=True)
    order = models.IntegerField(null=True)

