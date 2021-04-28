from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render


def about(request):
    return render(request, 'about.html')

def catalog(request):
    records = Record.objects.all()
    return render(request, 'catalog.html', {'records': records})

def account(request, username):
    return HttpResponse("You are not authorized to do that.")

def login(Request):
    return render(request, 'login.html')
