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
    is_logged_in = request.user.is_authenticated()
    c = {}
    c.update(csrf(request))
    print (request.user.username)
    context = {
        "innlogget": is_logged_in,
        "number": number,
        "c": c
    }
    return render_to_response('lockers/register.html', context)
