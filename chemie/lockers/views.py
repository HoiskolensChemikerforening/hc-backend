from django.shortcuts import render
from .models import Locker, LockerUser, Ownership, User
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.context_processors import csrf

def view_lockers(request):
    free_lockers = Locker.objects.filter(ownership__active=True)
    all_lockers = Locker.objects.all()
    occupied_lockers = Locker.objects.filter(ownership__active=False)
    context = {
        "lockers": free_lockers,
        "all": all_lockers,
        "occupied": occupied_lockers,
    }
    return render_to_response('lockers/list.html', context)

def register_locker(request, number):
    context = {
        "number": number,
    }

    if request.user.is_authenticated():
        if request.POST == True:
            # If the logged in user has confirmed locker
            locker = Locker.objects.get(pk=number)
            if not locker.is_free():
                locker_user = LockerUser.objects.get(internal_user=request.user)
                if locker_user:
                    pass
                    # Count this locker users' lockers and check that its lower than the limit
                else:
                    pass
                    # Create locker_user
                # Send mail
            else:
                pass
                # This is awkward. The locker is already in user
        else:
            pass
            # User has not clicked yes
            # Give a confirmation of sorts ?
            # This can probably be moved to a modal/popup during locker selection
    else:
        pass
        # User is not internal user
        form = ExternalRegisterLocker
        # Very simiilar logic to the one above
    return render_to_response('lockers/register.html', context)
