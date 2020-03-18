from django.shortcuts import render
from .models import RentalObject
from django.http import HttpResponse


def index(request):
    rentalObjects = RentalObject.objects.all().order_by("name")

    context={
        "rentalObjects" : rentalObjects
    }
    return render(request, "rentalservice/index.html", context)
