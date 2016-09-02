from django.utils import timezone
from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import RegisterEventForm, RegisterUserForm, DeRegisterUserForm
from .models import Event, Registration, REGISTRATION_STATUS, RegistrationMessage
from .email import send_event_mail


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
    all_events = Event.objects.filter(date__gt=timezone.now())
    context = {
        'events': all_events,
    }
    return render(request, "events/list.html", context)


# @cache_page(60 * 15)
def view_event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = {'first': ['Ida', 'Sevre', 'Erik', 'Ramn'], 'second': ['Martin', 'Inger Anna'], 'third': [],
                 'fourth': ['Amanda', 'Peter', 'Bjørn Erik'],
                 'fifth': ['Jonas', 'Jesus', 'Adnan']}
    context = {
        'event': event,
        'attendees': zip_longest(attendees['first'], attendees['second'], attendees['third'], attendees['fourth'],
                                 attendees['fifth'])
    }
    return render(request, "events/detail.html", context)


@login_required
def register_user(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration = Registration.objects.filter(event=event, user=request.user).first()
    form_init = {'enable_sleepover': event.sleepover,
                 'enable_night_snack': event.night_snack,
                 'enable_companion': event.companion}

    if request.POST:
        de_registration_form = DeRegisterUserForm(request.POST or None, prefix='deregister')
        edit_registration_form = RegisterUserForm(request.POST or None, prefix='edit', **form_init)
        registration_form = RegisterUserForm(request.POST or None, prefix='registration')
        if registration:
            # Change form being displayed as the user is registered
            registration_form = edit_registration_form
            if 'register_or_edit' in request.POST:
                if edit_registration_form.is_valid():
                    registration.night_snack = edit_registration_form.cleaned_data['night_snack']
                    registration.sleepover = edit_registration_form.cleaned_data['sleepover']
                    registration.companion = edit_registration_form.cleaned_data['companion']
                    registration.save()
                    messages.add_message(request, messages.SUCCESS, 'Påmeldingsdetaljene ble endret',
                                         extra_tags='Endringer utført')
                    return redirect(event)

            elif 'de_register' in request.POST and event.can_de_register:
                # Populate the registration form with registration data is it was not submitted
                registration_form = RegisterUserForm(instance=registration, prefix='edit', **form_init)
                if de_registration_form.is_valid():
                    lucky_person = Registration.objects.de_register(registration)
                    if lucky_person:
                        send_event_mail(lucky_person)
                    messages.add_message(request, messages.WARNING, 'Du er nå avmeldt {}'.format(event.title),
                                         extra_tags='Avmeldt')
                    return redirect(event)

        else:
            # User is not registered
            if registration_form.is_valid():
                instance = edit_registration_form.save(commit=False)
                instance.event = event
                instance.user = request.user
                instance.save()
                status = set_user_event_status(event, instance)

                if status == REGISTRATION_STATUS.CONFIRMED:
                    messages.add_message(request, messages.SUCCESS, 'Du er påmeld arrangementet.', extra_tags='Påmeldt')
                    send_event_mail(instance)
                    custom_messages = RegistrationMessage.objects.filter(user=instance.user, event=event)
                    for custom_message in custom_messages:
                        messages.add_message(request, messages.INFO, custom_message.message, extra_tags='PS')

                elif status == REGISTRATION_STATUS.WAITING:
                    messages.add_message(request, messages.WARNING, 'Arrangementet er fullt, men du er på venteliste.',
                                         extra_tags='Venteliste')
                    send_event_mail(instance)
                else:
                    # Denne bør ligge i en try-catch block
                    messages.add_message(request, messages.ERROR, 'En ukjent feil oppstod. Kontakt edb@hc.ntnu.no',
                                         extra_tags='Ukjent feil')
                # Edit was successful
                return redirect(event)
    else:
        registration_form, de_registration_form = None, None
        if (registration and event.can_de_register) or event.can_signup:
            # User can de-register or sign up
            form_prefix = 'registration' if registration is None else 'edit'
            registration_form = RegisterUserForm(prefix=form_prefix, instance=registration,
                                                 **form_init)
            de_registration_form = DeRegisterUserForm(None, prefix='deregister')

            if not registration:
                de_registration_form = None

    context = {
        "registration_form": registration_form,
        "event": event,
        "de_registration_form": de_registration_form,
        "registered": False if registration is None else True
    }
    return render(request, "events/register_user.html", context)


@login_required
@ensure_csrf_cookie
def view_admin_panel(request, event_id):
    if request.POST:
        if request.is_ajax():
            change_payment_status(request, event_id)
    event = Event.objects.get(pk=event_id)
    all_registrations = Registration.objects.filter(
        status=REGISTRATION_STATUS.CONFIRMED,
        event=event,
    ).prefetch_related('user__profile')

    context = {
        "attendees": all_registrations,
        "event": event,
    }
    return render(request, "events/admin_list.html", context)


@login_required
def change_payment_status(request, registration_id):
    # event = Event.objects.get(pk=event_id)
    registration = Registration.objects.get(pk=registration_id)
    payment_status = registration.payment_status
    registration.payment_status = not registration.payment_status
    registration.save()
    return JsonResponse({'payment_status': registration.payment_status})


@transaction.atomic
def set_user_event_status(event, registration):
    if event.has_spare_slots:
        registration.confirm()
        registration.save()
        return REGISTRATION_STATUS.CONFIRMED
    return REGISTRATION_STATUS.WAITING
