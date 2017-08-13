from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from .extras import MultiFormsView


from .email import send_event_mail
from .forms import RegisterEventForm, RegisterUserForm, DeRegisterUserForm, RegisterLimitations, RegisterBedpresForm
from .models import Event, EventRegistration, REGISTRATION_STATUS, RegistrationMessage, BaseRegistration, Limitation, Bedpres, BedpresRegistration


class CreateEventView(View):
    event_form = RegisterEventForm
    initial = None
    template_name = 'events/register_event.html'

    def get(self, request):
        context = {
            'form': self.event_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.event_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse('events:index'))
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class CreateBedpresView(View):
    bedpres_form = RegisterBedpresForm
    limitation_form = formset_factory(RegisterLimitations, extra=1)
    initial = None
    template_name = 'events/register_bedpres.html'

    def get(self, request):
        context = {
            'regform': self.bedpres_form,
            'formset': self.limitation_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.bedpres_form(request.POST, request.FILES)
        limitations = self.limitation_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            for limitation in limitations:
                if not limitation.is_valid():
                    context = {
                        'regform': form,
                        'formset': limitations,
                    }
                    return render(request, self.template_name, context)
                slots = limitation.cleaned_data.get('slots')
                grade = limitation.cleaned_data.get('grade')
                try:
                    lim_instance = Limitation.objects.create(slots=slots, grade=grade)
                    instance.limitations.add(lim_instance)
                except IntegrityError:
                    continue
            if instance.limitations_exceeds_total_slots:
                Bedpres.objects.get(pk=instance.id).delete()
                context = {
                    'regform': form,
                    'formset': limitations,
                }
                return render(request, self.template_name, context)
            return HttpResponseRedirect(reverse('events:index_bedpres'))
        context = {
            'regform': form,
            'formset': limitations,
        }
        return render(request, self.template_name, context)


class ListEventsView(View):
    template_name = 'events/overview.html'
    event_or_bedpres = 'event'

    def get(self, request):
        event_or_bedpres = self.event_or_bedpres
        template_name = self.template_name
        if event_or_bedpres == 'event':
            future_events = Event.objects.filter(date__gt=timezone.now()).order_by('date')
            my_events = Event.objects.filter(attendees__username__exact=request.user)
        elif event_or_bedpres == 'bedpres':
            future_events = Bedpres.objects.filter(date__gt=timezone.now()).order_by('date')
            my_events = Bedpres.objects.filter(attendees__username__exact=request.user)
        else:
            future_events = None
            my_events = None
        context = {
            'events': future_events,
            'my_events': my_events,
        }
        return render(request, template_name, context)


class ListPastEventsView(View):
    template_name = 'events/overview_past.html'
    event_or_bedpres = 'event'

    def get(self, request):
        event_or_bedpres = self.event_or_bedpres
        template_name = self.template_name
        if event_or_bedpres == 'event':
            past_events = Event.objects.filter(date__lte=timezone.now()).order_by('date')
        elif event_or_bedpres == 'bedpres':
            past_events = Bedpres.objects.filter(date__lte=timezone.now()).order_by('date')
        else:
            past_events = None
        context = {
            'events': past_events,
        }
        return render(request, template_name, context)


class ListWithDeleteView(View):
    template_name = 'events/delete.html'
    event_or_bedpres = 'event'

    def get(self, request):
        if self.event_or_bedpres == 'event':
            all_events = Event.objects.filter(date__gt=timezone.now())
        elif self.event_or_bedpres == 'bedpres':
            all_events = Bedpres.objects.filter(date__gt=timezone.now())
        else:
            all_events = None
        context = {
            'events': all_events,
        }
        return render(request, self.template_name, context)


class DeleteEventView(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse('events:delete')


class DeleteBedpresView(DeleteView):
    model = Bedpres

    def get_success_url(self):
        return reverse('events:delete_bedpres')


class ViewEventDetailsView(View):
    template_name = 'events/detail.html'
    event_or_bedpres = 'event'

    def get(self, request, pk):
        if self.event_or_bedpres == 'event':
            event = get_object_or_404(Event, pk=pk)
            registrations = EventRegistration.objects.filter(event=event, status=1).prefetch_related('user__profile')
        elif self.event_or_bedpres == 'bedpres':
            event = get_object_or_404(Bedpres, pk=pk)
            registrations = BedpresRegistration.objects.filter(event=event, status=1).prefetch_related('user__profile')
        else:
            raise Http404('Vi klarte dessverre ikke finne siden. Den matchet hverken bedpres eller arrangement')
        first, second, third, fourth, fifth, done = [], [], [], [], [], []
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
        return render(request, self.template_name, context)


class BaseRegisterUserView(SingleObjectMixin, View):
    model = Event

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object. This is run very early
        self.object = self.get_object()
        self.registration = EventRegistration.objects.filter(event=self.object, user=self.request.user).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        # Fetch event object
        event = self.object
        registration = EventRegistration.objects.filter(event=event, user=request.user).first()
        if registration:
                return EditRemoveUserRegistration.as_view()(self.request, object=event, registration=registration)
        else:
            if request.method == 'POST':
                return RegisterUserView.post(RegisterUserView(), request, self.object.pk)
            else:
                return RegisterUserView.as_view()(self.request, pk=pk)

    def post(self, request, pk):
        return self.get(request, pk)


class RegisterUserView(SingleObjectMixin, View):
    template_name = "events/register_user.html"
    model = Event

    pk = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object. This is run very early
        self.object = self.get_object()
        return super().dispatch(request, self.pk)

    def get_object(self, queryset=None):
        self.pk = self.kwargs.get('pk')
        return Event.objects.get(pk=self.pk)

    def get(self, request, pk, *args, **kwargs):
        if self.object.can_signup:
            registration_form = RegisterUserForm(**{
                'enable_sleepover': self.object.sleepover,
                'enable_night_snack': self.object.night_snack,
                'enable_companion': self.object.companion,
            })
        else:
            registration_form = None
        context = {
            "registration_form": registration_form,
            "event": self.object,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        registration_form = RegisterUserForm(request.POST)
        event = get_object_or_404(Event, pk=pk)
        if registration_form.is_valid():
            instance = registration_form.save(commit=False)
            instance.event = event
            instance.user = request.user
            instance.save()
            status = set_user_event_status(event, instance)
            self.set_status_message(request, status, instance, event)
            return redirect(reverse('events:register', kwargs={'pk': pk}))
        context = {
            'registration_form': registration_form,
            'event': event,
        }
        return render(request, self.template_name, context)

    @staticmethod
    def set_status_message(request, status, instance, event):
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


class EditRemoveUserRegistration(SingleObjectMixin, MultiFormsView):
    model = Event
    template_name = 'events/deregister_or_edit.html'
    form_classes = {'deregister': DeRegisterUserForm,
                    'edit': RegisterUserForm}
    success_url = 'event:register'

    registration = None
    object = None

    def get_edit_initial(self):
        # The boolean fields must be passed to the form along with any instance of current model
        return {'enable_sleepover': self.object.sleepover,
                'enable_night_snack': self.object.night_snack,
                'enable_companion': self.object.companion,
                'instance': self.registration}

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object. This is run very early
        self.object = self.get_object()
        self.registration = EventRegistration.objects.filter(event=self.object, user=self.request.user).first()
        return super().dispatch(request)

    def get_object(self, queryset=None):
        obj = self.kwargs.get('object')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(super(EditRemoveUserRegistration, self).get_context_data(**kwargs))

        # Remove the forms whenever the deadline has passed
        if not self.object.can_de_register:
            context.pop('deregister')
            context.pop('edit')

        # Add queue position
        registration = self.registration
        if registration:
            queue_position = EventRegistration.objects.filter(event=registration.event,
                                                              created__lt=registration.created,
                                                              status=REGISTRATION_STATUS.WAITING).count() + 1
            context.update({'queue_position': queue_position})
        return context

    def deregister_form_valid(self, form):
        event = self.object

        # Register the current user and give a slot to the first user in the event queue
        if event.can_de_register:
            registration = EventRegistration.objects.filter(event=event, user=self.request.user).first()
            lucky_person = EventRegistration.objects.de_register(registration)
            if lucky_person:
                send_event_mail(lucky_person, event)
            messages.add_message(self.request, messages.WARNING, 'Du er nå avmeldt {}'.format(event.title),
                                 extra_tags='Avmeldt')
        return redirect(event.get_absolute_registration_url())

    def edit_form_valid(self, form):
        # Form fields must be set as None is not a valid option
        registration = self.registration
        registration.night_snack = form.cleaned_data.get('night_snack') or 0
        registration.sleepover = form.cleaned_data.get('sleepover') or 0
        registration.companion = form.cleaned_data.get('companion')
        registration.save()
        messages.add_message(self.request, messages.SUCCESS, 'Påmeldingsdetaljene ble endret',
                             extra_tags='Endringer utført')

        return redirect(registration.event.get_absolute_registration_url())

    def signup_form_valid(self, form):
        user = form.save(self.request)
        return form.signup(self.request, user, self.get_success_url())


@login_required
def register_user_bedpres(request, event_id):
    pass

@login_required
@ensure_csrf_cookie
def view_admin_panel(request, event_id):
    event = Event.objects.get(pk=event_id)
    all_registrations = EventRegistration.objects.filter(
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
