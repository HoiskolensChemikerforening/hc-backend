from django.shortcuts import render
from django.template import RequestContext
from events.models import Event
from django.utils import timezone

def index(request):
    all_events = Event.objects.filter(date__gt=timezone.now())
    context = {
        'events': all_events
    }
    return render(request, 'home/index.html', context)