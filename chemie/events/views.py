from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import DeleteView

from .email import send_event_mail
from .extras import MultiFormsView
from .forms import RegisterEventForm, SocialRegisterUserForm, DeRegisterUserForm, RegisterBedpresForm, \
    BedpresRegisterUserForm
from .models import Social, EventRegistration, REGISTRATION_STATUS, RegistrationMessage, Bedpres, \
    BedpresRegistration


class CreateEventView(View):
    event_form = RegisterEventForm
    initial = None
    template_name = 'events/social/register.html'

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
            return HttpResponseRedirect(reverse('events:index_social'))
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class CreateBedpresView(View):
    bedpres_form = RegisterBedpresForm
    initial = None
    template_name = 'events/bedpres/create.html'

    def get(self, request):
        context = {
            'regform': self.bedpres_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        bedpres_form = RegisterBedpresForm(request.POST, request.FILES)
        if bedpres_form.is_valid():
            allowed_grades = bedpres_form.cleaned_data.get('allowed_grades')
            instance = bedpres_form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(reverse('events:index_bedpres'))
        context = {
            'regform': bedpres_form,
        }
        return render(request, self.template_name, context)


class ListSocialView(View):
    template_name = 'events/social/list.html'

    def get_objects(self, request):
        future_events = Social.objects.filter(date__gt=timezone.now(), published=True).order_by('date')
        my_events = Social.objects.filter(attendees__username__exact=request.user)
        return future_events, my_events

    def get(self, request):
        future_events, my_events = self.get_objects(request)
        context = {
            'events': future_events,
            'my_events': my_events,
        }
        return render(request, self.template_name, context)


class ListBedpresView(ListSocialView):
    template_name = 'events/bedpres/list.html'

    def get_objects(self, request):
        future_events = Bedpres.objects.filter(date__gt=timezone.now(), published=True).order_by('date')
        my_events = Bedpres.objects.filter(attendees__username__exact=request.user)
        return future_events, my_events


class ListPastSocialView(View):
    template_name = 'events/social/list_past.html'

    def get_objects(self):
        return Social.objects.filter(date__lte=timezone.now()).order_by('date')

    def get(self, request):
        past_events = self.get_objects().filter(published=True)
        context = {
            'events': past_events,
        }
        return render(request, self.template_name, context)


class ListPastBedpresView(ListPastSocialView):
    template_name = 'events/bedpres/list_past.html'

    def get_objects(self):
        return Bedpres.objects.filter(date__lte=timezone.now()).order_by('date')


class ListSocialDeleteView(View):
    template_name = 'events/social/delete.html'

    def get_objects(self):
        return Social.objects.filter(date__gt=timezone.now())

    def get(self, request):
        all_events = self.get_objects().filter(published=True)
        context = {
            'events': all_events,
        }
        return render(request, self.template_name, context)


class ListBedpresDeleteView(ListSocialDeleteView):
    def get_objects(self):
        return Bedpres.objects.filter(date__gt=timezone.now())


class DeleteSocialView(DeleteView):
    model = Social

    def get_success_url(self):
        return reverse('events:delete_list_social')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.published = False
        self.object.save()
        messages.add_message(request, messages.WARNING, 'Arrangementet ble slettet', extra_tags='Slettet')
        return HttpResponseRedirect(success_url)


class DeleteBedpresView(DeleteSocialView):
    model = Bedpres

    def get_success_url(self):
        return reverse('events:delete_list_bedpres')


class ViewSocialDetailsView(View):
    template_name = 'events/social/detail.html'

    def get_objects(self, pk):
        event = get_object_or_404(Social, pk=pk)
        registrations = EventRegistration.objects.filter(event=event, status=1).prefetch_related('user__profile')
        return event, registrations

    def get(self, request, pk):
        event, registrations = self.get_objects(pk)

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


class ViewBedpresDetailsView(ViewSocialDetailsView):
    template_name = 'events/bedpres/detail.html'

    def get_objects(self, pk):
        event = get_object_or_404(Bedpres, pk=pk)
        registrations = BedpresRegistration.objects.filter(event=event, status=1).prefetch_related('user__profile')
        return event, registrations


class SocialEditRemoveUserRegistration(SingleObjectMixin, MultiFormsView):
    model = Social
    registration_model = EventRegistration
    template_name = 'events/social/deregister_or_edit.html'
    form_classes = {'deregister': DeRegisterUserForm,
                    'edit': SocialRegisterUserForm}
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
        self.registration = self.registration_model.objects.filter(event=self.object, user=self.request.user).first()
        return super().dispatch(request)

    def get_object(self, queryset=None):
        obj = self.kwargs.get('object')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(super().get_context_data(**kwargs))

        # Remove the forms whenever the deadline has passed
        if not self.object.can_de_register:
            context.pop('deregister')
            if context.get('edit'):
                context.pop('edit')

        # Add queue position
        registration = self.registration
        if registration:
            queue_position = self.registration_model.objects.filter(event=registration.event,
                                                              created__lt=registration.created,
                                                              status=REGISTRATION_STATUS.WAITING).count() + 1
            context.update({'queue_position': queue_position})
        return context

    def deregister_form_valid(self, form):
        event = self.object

        # Deregister the current user and give a slot to the first user in the event queue
        if event.can_de_register:
            registration = self.registration_model.objects.filter(event=event, user=self.request.user).first()
            lucky_person = self.registration_model.objects.de_register(registration)
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


class BedpresEditRemoveUserRegistration(SocialEditRemoveUserRegistration):
    model = Bedpres
    registration_model = BedpresRegistration
    template_name = 'events/bedpres/deregister_or_edit.html'
    form_classes = {'deregister': DeRegisterUserForm}

    def get_edit_initial(self):
        return {'instance': self.registration}


class SocialRegisterUserView(SingleObjectMixin, View):
    template_name = "events/register_user.html"
    model = Social
    registration_form = SocialRegisterUserForm

    pk = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object. This is run very early
        self.object = self.get_object()
        return super().dispatch(request, self.pk)

    def get_object(self, queryset=None):
        self.pk = self.kwargs.get('pk')
        return self.model.objects.get(pk=self.pk)

    def get_form_kwargs(self):
        return {
            'enable_sleepover': self.object.sleepover,
            'enable_night_snack': self.object.night_snack,
            'enable_companion': self.object.companion,
        }

    def get(self, request, pk, *args, **kwargs):
        if self.object.can_signup:
            registration_form = self.registration_form(**self.get_form_kwargs())
        else:
            registration_form = None
        context = {
            "registration_form": registration_form,
            "event": self.object,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        registration_form = self.registration_form(request.POST)
        event = get_object_or_404(self.model, pk=pk)
        if registration_form.is_valid():
            instance = registration_form.save(commit=False)
            instance.event = event
            instance.user = request.user
            instance.save()
            status = set_user_event_status(event, instance)
            self.set_status_message(request, status, instance, event)
            return redirect(reverse('events:register_social', kwargs={'pk': pk}))
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


class BedpresRegisterUserView(SocialRegisterUserView):
    template_name = 'events/register_user.html'
    model = Bedpres


    registration_form = BedpresRegisterUserForm

    def get_form_kwargs(self):
        return {}


class SocialBaseRegisterUserView(SingleObjectMixin, View):
    model = Social
    registration_model = EventRegistration
    registration_view_edit = SocialEditRemoveUserRegistration
    registration_view_register = SocialRegisterUserView

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object. This is run very early
        self.object = self.get_object()
        self.registration = self.registration_model.objects.filter(event=self.object, user=self.request.user).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        # Fetch event object
        event = self.object
        registration = self.registration_model.objects.filter(event=event, user=request.user).first()

        if registration:
                return self.registration_view_edit.as_view()(self.request, object=event, registration=registration)
        else:
            if request.method == 'POST':
                return self.registration_view_register.post(self.registration_view_register(), request, self.object.pk)
            else:
                return self.registration_view_register.as_view()(self.request, pk=pk)

    def post(self, request, pk):
        return self.get(request, pk)


class BedpresBaseRegisterUserView(SocialBaseRegisterUserView):
    model = Bedpres
    registration_model = BedpresRegistration
    registration_view_edit = BedpresEditRemoveUserRegistration
    registration_view_register = BedpresRegisterUserView


@login_required
@ensure_csrf_cookie
def view_admin_panel(request, pk):
    event = Social.objects.get(pk=pk)
    all_registrations = EventRegistration.objects.filter(
        event=event,
    ).select_related('user__profile__membership')

    context = {
        "attendees": all_registrations,
        "event": event,
    }
    return render(request, "events/admin_list.html", context)


class SocialEnlistedUsersView(DetailView, View):
    template_name = 'events/admin_list.html'
    model = Social
    registration_model = EventRegistration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['attendees'] = self.registration_model.objects.filter(
            status=REGISTRATION_STATUS.CONFIRMED,
            event=self.object,
        ).select_related('user__profile__membership')

        return context


class BedpresEnlistedUsersView(SocialEnlistedUsersView):
    template_name = 'events/admin_list.html'
    model = Bedpres
    registration_model = BedpresRegistration


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
