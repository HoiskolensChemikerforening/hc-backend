from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from .email import send_event_mail
from .forms import RegisterEventForm, RegisterUserForm, DeRegisterUserForm, RegisterLimitations
from .models import Event, EventRegistration, REGISTRATION_STATUS, RegistrationMessage, BaseRegistration


@login_required
def create_event(request):
    form = RegisterEventForm(request.POST or None, request.FILES or None)
    limitation_formset = formset_factory(RegisterLimitations)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse('events:index'))
    context = {
        'form': form,
        'formset': limitation_formset,
    }
    return render(request, 'events/register_event.html', context)


def list_events(request):
    future_events = Event.objects.filter(date__gt=timezone.now()).order_by('date')
    my_events = None
    if request.user:
        my_events = Event.objects.filter(attendees__username__exact=request.user)
    context = {
        'events': future_events,
        'my_events': my_events,
    }
    return render(request, "events/overview.html", context)


def list_past_events(request):
    past_events = Event.objects.filter(date__lte=timezone.now()).order_by('date')

    context = {
        'events': past_events,
    }
    return render(request, "events/overview_past.html", context)


def list_with_delete(request):
    all_events = Event.objects.filter(date__gt=timezone.now())
    context = {
        'events': all_events,
    }
    return render(request, "events/delete.html", context)


def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.add_message(request, messages.SUCCESS, 'Arrangementet er slettet.')
        return HttpResponseRedirect(reverse('events:delete'))
    messages.add_message(request, messages.ERROR, 'Yiiiihaaa.')
    return render(request, 'events/delete.html')


# @cache_page(60 * 15)
def view_event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    first, second, third, fourth, fifth, done = [], [], [], [], [], []
    registrations = EventRegistration.objects.filter(event=event, status=1).prefetch_related('user__profile')
    for registration in registrations:
        if registration.user.profile.grade == 1:
            first.append(registration.user.get_full_name())
        if registration.user.profile.grade == 2:
            second.append(registration.user.get_full_name())
        if registration.user.profile.grade == 3:
            third.append(registration.user.get_full_name())
        if registration.user.profile.grade == 4:
            fourth.append(registration.user.get_full_name())
        if registration.user.profile.grade == 5:
            fifth.append(registration.user.get_full_name())
        if registration.user.profile.grade == 6:
            done.append(registration.user.get_full_name())

    attendees = {
        'first': first,
        'second': second,
        'third': third,
        'fourth': fourth,
        'fifth': fifth,
        'done': done,
    }

    context = {
        'event': event,
        'attendees': zip_longest(attendees['first'], attendees['second'], attendees['third'],
                                 attendees['fourth'], attendees['fifth'], attendees['done'], ),
    }
    return render(request, "events/detail.html", context)


# attendees = {'first': ['Ida', 'Sevre', 'Erik', 'Ramn'], 'second': ['Martin', 'Inger Anna'], 'third': [],
#             'fourth': ['Amanda', 'Peter', 'Bjørn Erik'],
#             'fifth': ['Jonas', 'Jesus', 'Adnan']}
# context = {
#    'event': event,
#    'attendees': zip_longest(attendees['first'], attendees['second'], attendees['third'], attendees['fourth'],
#                             attendees['fifth'])

@login_required
def register_user(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    queue_position = None
    if registration:
        queue_position = EventRegistration.objects.filter(event=registration.event,
                                                          created__lt=registration.created,
                                                          status=REGISTRATION_STATUS.WAITING).count() + 1

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
                    registration.night_snack = edit_registration_form.cleaned_data.get('night_snack') or 0
                    registration.sleepover = edit_registration_form.cleaned_data.get('sleepover') or 0
                    registration.companion = edit_registration_form.cleaned_data.get('companion')
                    registration.save()
                    messages.add_message(request, messages.SUCCESS, 'Påmeldingsdetaljene ble endret',
                                         extra_tags='Endringer utført')
                    return redirect(event)

            elif 'de_register' in request.POST and event.can_de_register:
                # Populate the registration form with registration data is it was not submitted
                registration_form = RegisterUserForm(instance=registration, prefix='edit', **form_init)
                if de_registration_form.is_valid():
                    lucky_person = EventRegistration.objects.de_register(registration)
                    if lucky_person:
                        send_event_mail(lucky_person, event)
                    messages.add_message(request, messages.WARNING, 'Du er nå avmeldt {}'.format(event.title),
                                         extra_tags='Avmeldt')
                    return redirect(event)

        else:
            # User is not registered
            if registration_form.is_valid():
                instance = registration_form.save(commit=False)
                instance.event = event
                instance.user = request.user
                instance.save()
                status = set_user_event_status(event, instance)

                if status == REGISTRATION_STATUS.CONFIRMED:
                    messages.add_message(request, messages.SUCCESS, 'Du er påmeldt arrangementet.', extra_tags='Påmeldt')
                    send_event_mail(instance, event)
                    custom_messages = RegistrationMessage.objects.filter(user=instance.user, event=event)
                    for custom_message in custom_messages:
                        messages.add_message(request, messages.INFO, custom_message.message, extra_tags='PS')

                elif status == REGISTRATION_STATUS.WAITING:
                    messages.add_message(request, messages.WARNING, 'Arrangementet er fullt, men du er på venteliste.',
                                         extra_tags='Venteliste')
                    send_event_mail(instance, event)
                else:
                    # Denne bør ligge i en try-catch block
                    messages.add_message(request, messages.ERROR, 'En ukjent feil oppstod. Kontakt edb@hc.ntnu.no',
                                         extra_tags='Ukjent feil')
                # Edit was successful
                return redirect(event)
    else:
        registration_form, de_registration_form = None, None
        if (registration and event.can_de_register) or (event.can_signup and not registration):
            # User can de-register or sign up
            form_prefix = 'registration' if registration is None else 'edit'
            registration_form = RegisterUserForm(prefix=form_prefix, instance=registration,
                                                 **form_init)
            de_registration_form = DeRegisterUserForm(None, prefix='deregister')

            if not registration:
                de_registration_form = None

    context = {
        "registration": registration,
        "queue_position": queue_position,
        "registration_form": registration_form,
        "event": event,
        "de_registration_form": de_registration_form,
        "registered": False if registration is None else True
    }
    return render(request, "events/register_user.html", context)


@login_required
@ensure_csrf_cookie
def view_admin_panel(request, event_id):
    event = Event.objects.get(pk=event_id)
    all_registrations = EventRegistration.objects.filter(
        status=REGISTRATION_STATUS.CONFIRMED,
        event=event,
    ).select_related('user__profile__membership')
    context = {
        "attendees": all_registrations,
        "event": event,
    }
    return render(request, "events/admin_list.html", context)


@login_required
@permission_required('events.change_eventregistration')
def change_payment_status(request, registration_id):
    registration = EventRegistration.objects.get(pk=registration_id)
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