from django.shortcuts import render
from .models import Locker, Ownership, User
from django.shortcuts import render_to_response, get_object_or_404, render

def view_lockers(request):
    free_lockers = Locker.objects.filter(ownerships__active=True)
    context = {
        "lockers": free_lockers
    }
    return render_to_response('elections/list.html', context)