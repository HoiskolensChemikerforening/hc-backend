from django.shortcuts import render
from .forms import RegisterEventForm, RegisterUserForm
from django.contrib.auth.decorators import login_required
from .models import Event, Registration, REGISTRATION_STATUS
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from itertools import zip_longest
from django.db import transaction
from django.views.decorators.cache import cache_page

@login_required
def create_event(request):
    form = RegisterEventForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
    context = {
        'form': form,
    }
    return render(request, 'events/register_event.html', context)

def list_all(request):
    all_events = Event.objects.filter(date__gt=datetime.now())
    context = {
        'events': all_events,
    }
    return render(request, "events/list.html", context)

#@cache_page(60 * 15)
def view_event_details(request, event_id):
    event = get_object_or_404(Event,pk=event_id)
    attendees = {'first': ['Ida', 'Sevre', 'Erik', 'Ramn'], 'second':['Martin', 'Inger Anna'], 'third': [], 'fourth':['Amanda', 'Peter', 'Bjørn Erik'],
                 'fifth':['Jonas', 'Jesus', 'Adnan']}
    context = {
        'event' : event,
        'attendees': zip_longest(attendees['first'], attendees['second'], attendees['third'], attendees['fourth'], attendees['fifth'])
    }
    return render(request, "events/detail.html", context)

@login_required
def register_user(request, event_id):
    event = get_object_or_404(Event,pk=event_id)
    registered =    Registration.objects.filter(event=event, user=request.user)
    status = None
    if registered:
        if request.POST:
            messages.add_message(request, messages.ERROR, 'Du er allerede påmeldt.', extra_tags='Ulovlig operasjon')
        registration = None
    else:
        registration = RegisterUserForm(request.POST or None)
        if registration.is_valid():
            instance = registration.save(commit=False)
            instance.event = event
            instance.user = request.user
            instance.save()
            status = set_user_event_status(event, instance)

            if status == REGISTRATION_STATUS.CONFIRMED:
                messages.add_message(request, messages.SUCCESS, 'Du er påmeld arrangementet.', extra_tags='Påmeldt')
                # Send mail
            elif status == REGISTRATION_STATUS.WAITING:
                messages.add_message(request, messages.WARNING, 'Arrangementet er fullt, men du er på venteliste.', extra_tags='Venteliste')
            else:
                # Denne bør ligge i en try-catch block
                messages.add_message(request, messages.ERROR, 'En ukjent feil oppstod. Kontakt edb@hc.ntnu.no', extra_tags='Ukjent feil')

    context = {
        "registration_form": registration or None,
        "event" : event,
        "status": status,
    }
    return render(request, "events/register_user.html", context)

@login_required
def view_admin_panel(request, event_id):
    event = Registration.objects.get(pk=event_id)
    all_registrations = Registration.objects.filter(
        status=REGISTRATION_STATUS.CONFIRMED,
        event=event,
        ).prefetch_related('user__profile')

    context = {
        "attendees" : all_registrations,
    }
    render(request, "events/admin_list.html", context)








@login_required()
def de_register_user(request, event_id):
    if request.POST:
        event = Event.objects.get(pk=event_id)
        registration = Registration.objects.get(event=event, user=request.user)
        lucky_person = Registration.objects.de_register(event, registration)
        if lucky_person:
            # Send mail
            pass

@transaction.atomic
def set_user_event_status(event, registration):
    if event.has_spare_slots():
        registration.confirm()
        registration.save()
        return REGISTRATION_STATUS.CONFIRMED
    return REGISTRATION_STATUS.WAITING

