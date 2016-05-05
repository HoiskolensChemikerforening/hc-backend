from .models import Locker, LockerUser, Ownership, LockerConfirmation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from .forms import RegisterExternalLockerUserForm, RegisterInternalLockerUserForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

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


def register_locker_external(request, number):
    # Fetch requested locker
    locker = Locker.objects.get(number=number)
    if not locker.is_free():
        # Locker was already taken
        raise Http404

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

        # Create a new ownership for the user
        new_ownership = Ownership.objects.create(locker=locker, user=user)

        # Create confirmation link object
        confirmation_object = LockerConfirmation.objects.create(ownership=new_ownership)

        context  = {
            "confirmation": confirmation_object,
            "user": user,
            "ownership": new_ownership,
        }

        render(request, 'lockers/almostDone.html', context)

    context = {
        "form": form,
    }
    return render(request, 'lockers/register2.html', context)


def register_locker_internal(request, number):
    pass


def register_locker(request, number):
    if Locker.objects.get(number=number).is_free():
        if request.user.is_authenticated():
            return(register_locker_external(request, number))
        else:
            # Internal
            return(register_locker_external(request, number))
    else:
        raise Http404



    # context = {
    #     "number": number,
    # }
    #
    # if request.user.is_authenticated():
    #     if request.POST == True:
    #         # If the logged in user has confirmed locker
    #         locker = Locker.objects.get(pk=number)
    #         if not locker.is_free():
    #             locker_user = LockerUser.objects.get(internal_user=request.user)
    #             if locker_user:
    #                 pass
    #                 # Count this locker users' lockers and check that its lower than the limit
    #             else:
    #                 pass
    #                 # Create locker_user
    #             # Send mail
    #         else:
    #             pass
    #             # This is awkward. The locker is already in user
    #     else:
    #         pass
    #         # User has not clicked yes
    #         # Give a confirmation of sorts ?
    #         # This can probably be moved to a modal/popup during locker selection
    # else:
    #     pass
    #     # User is not internal user
    #     form = RegisterExternalLockerUserForm
    #     # Very simiilar logic to the one above
    # return render(request, 'lockers/register.html', context)

