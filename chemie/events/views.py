from django.shortcuts import render
from . import Event
# Create your views here.

def RegisterEvent(request):
    form = request.POST or None
    if request.POST:
        

    context = []
    return render(request, 'event/register_event.html', context)