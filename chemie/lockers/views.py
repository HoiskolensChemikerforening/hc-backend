from .models import Locker, LockerUser, Ownership, LockerConfirmation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from .forms import RegisterExternalLockerUserForm, RegisterInternalLockerUserForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from customprofile.models import Profile
from .email import queue_activation_mail


def view_lockers(request, page=0):
    locker_list = Locker.objects.all()
    paginator = Paginator(locker_list, 20)

    try:
        lockers = paginator.page(page)
    except PageNotAnInteger:
        lockers = paginator.page(1)
    except EmptyPage:
        lockers = paginator.page(paginator.num_pages)

    context = {
        "lockers": lockers,
    }
    return render(request, 'lockers/list.html', context)


def bind_user_locker(request, locker, user):
        # Create a new ownership for the user
        new_ownership = Ownership.objects.create(locker=locker, user=user)
        new_ownership.save()

        # Create confirmation link object
        confirmation_object = LockerConfirmation.objects.create(ownership=new_ownership)
        confirmation_object.save()

        context  = {
            "confirmation": confirmation_object,
            "locker_user": user,
            "ownership": new_ownership,
            "request":request
        }
        queue_activation_mail(context, 'emails/activation.html')
        return render(request, 'lockers/almostDone.html', context)


def register_locker_external(request, locker):
    form = RegisterExternalLockerUserForm(request.POST or None)

    if form.is_valid():
        # Check if user already exists
        instance = form.save(commit=False)
        try:
            user = LockerUser.objects.get(username=instance.username)
        except ObjectDoesNotExist:
            # User not found. Create user
            instance.save()
            user = instance

        if user.reached_limit():
            # User has reached the active locker limit
            raise Http404

        return bind_user_locker(request, locker, user)

    context = {
        "form": form,
    }
    return render(request, 'lockers/registrer.html', context)


def register_locker_internal(request, locker):
    auth_user = request.user
    if auth_user.is_authenticated():
        # Check if user already exists

        try:
            user = LockerUser.objects.get(internal_user=auth_user)
        except ObjectDoesNotExist:
            # User not found. Create user
            locker_user = LockerUser.objects.create(internal_user=auth_user)
            locker_user.save()
            user = locker_user

        if user.reached_limit():
            # User has reached the active locker limit
            raise Http404

        return bind_user_locker(request, locker, user)


def register_locker(request, number):
        # Fetch requested locker
    locker = Locker.objects.get(number=number)
    if not locker.is_free():
        # Locker was already taken
        raise Http404
    else:
        if request.user.is_authenticated():
            # Internal
            return register_locker_internal(request, locker)
        else:
            # External
            return register_locker_external(request, locker)


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

def reset_locker_ownerships(request):
    # Oh boi where to start... definite_owner is the related name between Ownership and
    # Locker, it lets us collect all Lockers where "owner" definite link is set (__isnull=False).
    # Finally, we filter all ownerships that are connected to these Lockers (with its "weak" link)
    ownerships_to_reset = Ownership.objects.filter(definite_owner__owner__isnull=False).prefetch_related("user")

    for ownership in ownerships_to_reset:
        ownership.is_active = False
        confirmation_object = LockerConfirmation.objects.create(ownership=ownership)
        confirmation_object.save()

        context  = {
            "confirmation": confirmation_object,
            "locker_user": ownership.user,
            "ownership": ownership,
            "request": request
        }
        queue_activation_mail(context, 'emails/reactivate.html')


def reset_unconfirmed_lockers(request):
    pass