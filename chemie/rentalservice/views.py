from django.shortcuts import render, redirect
from .models import RentalObject
from django.http import HttpResponse
from .forms import RentalObjectForm


def index(request):
    rentalObjects = RentalObject.objects.all().order_by("name")

    context = {"rentalObjects": rentalObjects}
    return render(request, "rentalservice/index.html", context)


def new_object(request):
    form = RentalObjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("rentalservice:index")

    context = {"form": form}
    return render(request, "rentalservice/new_object.html", context)
