from django.shortcuts import render
from .forms import RegisterEvent
from django.contrib.auth.decorators import login_required
from .models import Event
from datetime import datetime
# Create your views here.

@login_required
def register_event(request):
    form = RegisterEvent(request.POST or None)
    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
    context = {
        'form': form,
    }
    return render(request, 'events/register_event.html', context)

def list(request):
    all_events = Event.objects.filter(date__gt=datetime.now())
    context = {
        'events': all_events,
    }
    return render(request, "events/list.html", context)

#def index(request):
#    event = request's ID to specific event
#    context = {
#        'event': event
#    return render(request, "events/index.html", context)

# This view is supposed to view more info about a
# specific event if you click its title