from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import RentalObject
from .forms import RentalObjectForm


def index(request):
    rentalObjects = RentalObject.objects.all().order_by("name")

    context = {"rentalObjects": rentalObjects}
    return render(request, "rentalservice/index.html", context)

@permission_required("rentalservice.new_object")
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

@permission_required("rentalservice.delete_rentalobject")
def delete_rentalobject(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, id=rentalobject_id)
    rental_object.delete()
    messages.add_message(
        request, messages.SUCCESS, "Utleieobjektet ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("rentalservice:index"))

@permission_required("rentalservice.change_rentalobject")
def edit_rentalobject(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, id=rentalobject_id)
    form = RentalObjectForm(
        request.POST or None, request.FILES or None, instance=rental_object
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Utleieobjekt ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("rentalservice:index"))
    context = {"form": form}

    return render(request, "rentalservice/new_object.html", context)