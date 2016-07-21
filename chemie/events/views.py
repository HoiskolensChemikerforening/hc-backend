from django.shortcuts import render
from .forms import RegisterEvent
from django.contrib.auth.decorators import login_required
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