from catalog.models import Record
from django.shortcuts import render


def about(request):
    return render(request, 'about.html')

def catalog(request):
    records = Record.objects.all()
    return render(request, 'catalog.html', {'records': records})