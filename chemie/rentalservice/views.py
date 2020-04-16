from django.shortcuts import render, redirect, get_object_or_404
from .models import RentalObject
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


def detail(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, id=rentalobject_id)
    context = {"rental_object": rental_object}
    return render(request, "rentalservice/detail.html", context)
