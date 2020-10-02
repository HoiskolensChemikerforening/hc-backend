from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .email import send_my_lockers_mail, send_activation_mail
from .forms import (
    RegisterExternalLockerUserForm,
    MyLockersForm,
    ConfirmOwnershipForm,
)
from .models import Locker, LockerUser, Ownership, LockerToken
from .serializers import LockerSerializer, LockerUserSerializer
from rest_framework import generics


def view_lockers(request):
    free_locker_list = Locker.objects.filter(
        owner__isnull=True
    ).prefetch_related("owner")
    free_lockers = Locker.objects.filter(owner__isnull=True).count()

    paginator = Paginator(free_locker_list, 40)
    page_number = request.GET.get("page", 1)

    try:
        locker_page = paginator.page(page_number)
    except PageNotAnInteger:
        locker_page = paginator.page(1)
    except EmptyPage:
        locker_page = paginator.page(paginator.num_pages)

    context = {"locker_page": locker_page, "free_lockers": free_lockers}
    return render(request, "lockers/list.html", context)


def my_lockers(request):
    form = MyLockersForm(request.POST or None)
    if request.POST:
        email = form.data.get("email")
        if form.is_valid():
            try:
                locker_user = LockerUser.objects.get(email=email)
                lockers = locker_user.fetch_lockers()
                if not len(lockers):
                    raise ObjectDoesNotExist

                send_my_lockers_mail(email, lockers, locker_user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Eposten ble sendt!",
                    extra_tags="Dine skap",
                )
                return redirect(reverse("frontpage:home"))
            except ObjectDoesNotExist:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Ingen bokskap ble funnet på denne eposten.",
                    extra_tags="Ikke funnet",
                )

    context = {"form": form}
    return render(request, "lockers/mineskap.html", context)


def register_locker(request, number):
    # Fetch requested locker
    locker = Locker.objects.get(number=number)

    if not locker.is_free():
        # Locker was already taken
        messages.add_message(
            request,
            messages.ERROR,
            "Skapet du prøver å registrere er allerede opptatt. "
            "Vennligst velg et annet skap",
            extra_tags="Bokskap opptatt",
        )

        return redirect(reverse("lockers:index"))

    else:
        form_data = RegisterExternalLockerUserForm(request.POST or None)
        if form_data.is_valid():
            # Check if user already exists
            user = form_data.save(commit=False)
            try:
                user = LockerUser.objects.get(email=user.email)
            except ObjectDoesNotExist:
                user.save()

            # Create a new ownership for the user
            new_ownership = Ownership(locker=locker, user=user)
            if new_ownership.reached_limit():
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Du har allerede to registrerte bokskap. "
                    "For å kunne reservere et nytt må du fjerne et av de gamle.",
                    extra_tags="For mange skap",
                )

                return redirect(reverse("lockers:index"))

            new_ownership.save()

            # Create confirmation link object
            token = new_ownership.create_confirmation()
            send_activation_mail(user, token)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Bokskapet er nesten reservert! "
                "En epost har blitt sendt til deg med videre instrukser for å bekrefte epostaddressen din.",
                extra_tags="Boskap - reservasjon",
            )

            return redirect(reverse("frontpage:home"))

        context = {"form": form_data}
        return render(request, "lockers/registrer.html", context)


def activate_ownership(request, code):
    try:
        activator = LockerToken.objects.get(key=code)
    except ObjectDoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            "Aktiveringsnøkkelen er allerede brukt eller har utgått.",
            extra_tags="Ugyldig nøkkel",
        )
        raise Http404
    agreed_to_terms = ConfirmOwnershipForm(request.POST or None)
    if request.method == "POST":
        if agreed_to_terms.is_valid():
            try:
                activator.activate()
            except ValidationError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Bokskapet ble reservert før du rakk å reservere det.",
                    extra_tags="Bokskap - opptatt",
                )
                return redirect(reverse("bokskap:index"))

            messages.add_message(
                request,
                messages.SUCCESS,
                "Bokskapet ble aktivert og er nå ditt =D",
                extra_tags="Fullført",
            )

            return redirect(reverse("frontpage:home"))

    return render(
        request,
        "lockers/confirm_locker.html",
        context={"form": agreed_to_terms},
    )


@permission_required("lockers.delete_locker")
def manage_lockers(request):
    lockers = (
        Locker.objects.prefetch_related("indefinite_locker__user")
        .prefetch_related("indefinite_locker__is_confirmed__exact=True")
        .select_related("owner__user")
    )
    context = {"request": request, "lockers": lockers}
    return render(request, "lockers/administrer.html", context)


@permission_required("lockers.delete_locker")
def clear_locker(request, locker_number):
    locker = get_object_or_404(Locker, number=locker_number)
    if locker.owner:
        locker.clear()
        locker.save()

    return redirect(
        reverse("bokskap:administrate") + "#locker{}".format(locker_number)
    )

class LockerListCreate(generics.ListCreateAPIView):
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer

class LockerUserListCreate(generics.ListCreateAPIView):
    queryset = LockerUser.objects.all()
    serializer_class = LockerUserSerializer
