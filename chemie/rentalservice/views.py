from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from post_office import mail

from .models import RentalObject, Landlord
from .forms import CreateRentalObjectForm, InvoiceForm, RentalObjectForm
from chemie.home.forms import ContactForm


def index(request):
    return render(request, "rentalservice/index_ac.html")


def index_promo(request):
    return render(request, "rentalservice/index_promo.html")


@login_required
def index_sportskom(request):
    rentalObjects = RentalObject.objects.filter(owner=3)

    rentalObjects = RentalObject.objects.all().order_by("name")
    if not rentalObjects.exists():
        return render(request, "/empty.html")

    obj_per_page = 12  # Show 24 contacts per page.
    if len(rentalObjects) < obj_per_page:
        context = {"rentalObjects": rentalObjects}
    else:
        paginator = Paginator(rentalObjects, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"rentalObjects": page_obj}
    return render(request, "rentalservice/index_sportskom.html", context)


@permission_required("rentalservice.add_rentalobject")
def new_object(request):
    form = CreateRentalObjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        
        messages.add_message(
        request,
        messages.SUCCESS,
        "Utleieobjektet ble opprettet",
        extra_tags="Opprettet",
    )
        return redirect("rentalservice:index_sportskom")

    context = {"new_obj_form": form}
    return render(request, "rentalservice/new_object.html", context)


@login_required
def detail(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, pk=rentalobject_id)
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
    return HttpResponseRedirect(reverse("rentalservice:index_sportskom"))


@permission_required("rentalservice.change_rentalobject")
def edit_rentalobject(request, rentalobject_id):
    rental_object = get_object_or_404(RentalObject, id=rentalobject_id)
    form = CreateRentalObjectForm(
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
            return HttpResponseRedirect(
                reverse("rentalservice:index_sportskom")
            )
    context = {"new_obj_form": form}

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

        mail_to = rental_object.owner.committee.email

        mail.send(
            mail_to,
            settings.DEFAULT_FROM_EMAIL,
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

        return redirect(reverse("rentalservice:index_ac"))

    else:
        context = {"contact_form": contact_form, "rentalobject": rental_object}

        return render(request, "rentalservice/contact.html", context)


@permission_required("rentalservice.add_rentalobject")
def new_invoice(request):
    form = InvoiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("rentalservice:index_ac")

    context = {"form": form}
    return render(request, "rentalservice/create_invoice.html", context)


def contact_page(request):
    return render(request, "rentalservice/contact_page_ac.html")


def contact_page_promo(request):
    return render(request, "rentalservice/contact_page_promo.html")


@login_required
def contact_page_sportskom(request):
    return render(request, "rentalservice/contact_sportskom.html")
