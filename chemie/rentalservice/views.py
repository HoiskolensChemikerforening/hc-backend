from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from post_office import mail


from .models import RentalObject
from .forms import RentalObjectForm
from chemie.home.forms import ContactForm


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
        request,
        messages.SUCCESS,
        "Utleieobjektet ble slettet",
        extra_tags="Slettet",
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


def contact(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, id=rentalobject_id)
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        messages.add_message(
            request,
            messages.SUCCESS,
            "Meldingen ble mottatt. Takk for at du tar kontakt!",
            extra_tags="Mottatt!",
        )

        _, mail_to = zip(*settings.CONTACTS)

        mail.send(
            mail_to,
            template="rental_contact",
            context={
                "rentalobject": rental_object,
                "message": contact_form.cleaned_data.get("content"),
                "contact_name": contact_form.cleaned_data.get("contact_name"),
                "contact_email": contact_form.cleaned_data.get(
                    "contact_email"
                ),
                "root_url": get_current_site(None),
            },
        )

        return redirect(reverse("rentalservice:index"))

    else:

        context = {"contact_form": contact_form, "rentalobject": rental_object}

        return render(request, "rentalservice/contact.html", context)
