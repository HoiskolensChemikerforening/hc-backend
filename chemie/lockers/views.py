from .models import Locker, LockerUser, Ownership, LockerConfirmation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import RegisterExternalLockerUserForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .email import queue_activation_mail
from django.contrib.auth.decorators import permission_required


def view_lockers(request, page=1):
    locker_list = Locker.objects.all()
    free_lockers = Locker.objects.filter(owner__isnull=True).count()
    paginator = Paginator(locker_list, 20)

    try:
        lockers = paginator.page(page)
    except PageNotAnInteger:
        lockers = paginator.page(1)
    except EmptyPage:
        lockers = paginator.page(paginator.num_pages)

    context = {
        "lockers": lockers,
        "free_lockers": free_lockers,
    }
    return render(request, 'lockers/list.html', context)


def register_locker(request, number):
    # Fetch requested locker
    locker = Locker.objects.get(number=number)
    if not locker.is_free():
        # Locker was already taken
        raise Http404
    else:
        form_data = RegisterExternalLockerUserForm(request.POST or None)
        if form_data.is_valid():
            # Check if user already exists
            instance = form_data.save(commit=False)
            user, _ = LockerUser.objects.get_or_create(username=instance.username)

            # Create a new ownership for the user
            new_ownership = Ownership(locker=locker, user=user)
            if new_ownership.reached_limit():
                raise Http404

            new_ownership.save()

            # Create confirmation link object
            confirmation_object = new_ownership.create_confirmation()

            context = {
                "confirmation": confirmation_object,
                "locker_user": user,
                "ownership": new_ownership,
                "request": request
            }

            queue_activation_mail(context, 'emails/activation.html')
            return render(request, 'lockers/almostDone.html', context)

        context = {
            "form": form_data,
        }
        return render(request, 'lockers/registrer.html', context)


def activate_ownership(request, code):
    try:
        activator = LockerConfirmation.objects.get(key=code)
        activator.activate()
    except ObjectDoesNotExist:
        raise Http404

    context = {
        "title": 'Fullført',
        "message": 'Bokskapet er nå ditt =D',
        "status": 'success',
    }
    return render(request, 'common/feedback.html', context)


@permission_required('lockers.can_delete')
def manage_lockers(request):
    lockers = Locker.objects.prefetch_related('indefinite_locker__is_confirmed__exact=True').prefetch_related(
         'indefinite_locker__user')
    context = {
        "request": request,
        "lockers": lockers
    }
    return render(request, 'lockers/administrer.html', context)


@permission_required('lockers.can_delete')
def reset_locker_ownerships(request):
    # Oh boi where to start... definite_owner is the related name between Ownership and
    # Locker, (Ownership -> Locker) it lets us collect all Lockers where "owner" definite link is set (__isnull=False).
    # Finally, we filter all ownerships that are connected to these Lockers (with its "weak" link)
    ownerships_to_reset = Ownership.objects.filter(definite_owner__owner__isnull=False).prefetch_related("user")

    for ownership in ownerships_to_reset:
        ownership.is_active = False
        ownership.save()
        confirmation_object = ownership.create_confirmation()

        context = {
            "confirmation": confirmation_object,
            "locker_user": ownership.user,
            "ownership": ownership,
            "request": request
        }
        queue_activation_mail(context, 'emails/reactivate.html')


@permission_required('lockers.can_delete')
def prune_expired_items(request):
    Ownership.objects.prune_expired()
    LockerConfirmation.objects.prune_expired()


@permission_required('lockers.can_delete')
def reset_idle_lockers(request):
    Locker.objects.reset_idle()


def administration_overview(request):
    Ownership.objects.fetch_all_states()
