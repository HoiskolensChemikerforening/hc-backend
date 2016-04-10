from django.shortcuts import render
from .models import Locker, Ownership, User
from django.shortcuts import render_to_response, get_object_or_404, render

def view_lockers(request):
    free_lockers = Locker.objects.filter(ownership__active=True)
    all_lockers = Locker.objects.all()
    occupied_lockers = Locker.objects.filter(ownership__active=False)
    context = {
        "lockers": free_lockers,
        "all": all_lockers,
        "occupied": occupied_lockers,
    }
    print (free_lockers)
    return render_to_response('lockers/list.html', context)
