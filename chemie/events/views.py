from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Q
from .email import send_event_mail
from .extras import MultiFormsView
from .forms import RegisterEventForm, SocialRegisterUserForm, DeRegisterUserForm, RegisterBedpresForm, \
    BedpresRegisterUserForm
from .models import Social, EventRegistration, REGISTRATION_STATUS, RegistrationMessage, Bedpres, \
    BedpresRegistration


class SuccessMessageMixin(object):
    message_content = '', '', ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        message_type, message, heading = self.message_content
        messages.add_message(self.request, message_type, message, extra_tags=heading)
        return response


class SocialFormView(FormView):
    template_name = 'events/social/create.html'
    form_class = RegisterEventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    class Meta:
        abstract = True


class CreateSocialView(PermissionRequiredMixin, SuccessMessageMixin, SocialFormView, CreateView):
    success_url = reverse_lazy('events:index_social')
    permission_required = 'events.add_event'
    # TODO: Couple the allowed grades with GRADES enum from customprofile models
    initial = {'allowed_grades': [1, 2, 3, 4, 5, 6]}
    success_message = "%(name)s was created successfully"
    message_content = messages.SUCCESS, 'Arrangementet ble opprettet', 'Opprettet'


class EditSocialView(PermissionRequiredMixin, SuccessMessageMixin, SocialFormView, UpdateView, ):
    permission_required = 'events.change_event'
    # Can't edit past events
    queryset = Social.objects.filter(date__gte=timezone.now())
    success_message = "%(name)s was created successfully"
    message_content = messages.SUCCESS, 'Arrangementet ble endret', 'Endret'


class BedpresFormView(SocialFormView):
    template_name = 'events/bedpres/create.html'
    form_class = RegisterBedpresForm


class CreateBedpresView(PermissionRequiredMixin, SuccessMessageMixin, BedpresFormView, CreateView):
    success_url = reverse_lazy('events:index_bedpres')
    permission_required = 'events.add_bedpres'
    message_content = messages.SUCCESS, 'Bedpresen ble opprettet', 'Opprettet'


class EditBedpresView(PermissionRequiredMixin, SuccessMessageMixin, BedpresFormView, UpdateView):
    permission_required = 'events.change_bedpres'
    # Can't edit past events
    queryset = Bedpres.objects.filter(date__gte=timezone.now())
    message_content = messages.SUCCESS, 'Bedpresen ble endret', 'Endret'


class ListSocialView(ListView):
    template_name = 'events/social/list.html'
    model = Social

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        future_events = self.model.objects.filter(date__gt=timezone.now(), published=True).order_by('date')

        my_events = None
        if self.request.user.is_authenticated:
            attending_events = Q(attendees__username__exact=self.request.user)
            authored_events = Q(author=self.request.user)
            my_events = self.model.objects.filter(attending_events | authored_events).distinct()

        context.update({
            'events': future_events,
            'my_events': my_events
        })
        return context


class ListBedpresView(ListSocialView):
    template_name = 'events/bedpres/list.html'
    model = Bedpres


class ListPastSocialView(ListView):
    template_name = 'events/social/list_past.html'
    model = Social

    def queryset(self):
        return self.model.objects.filter(date__lte=timezone.now()).order_by('date')


class ListPastBedpresView(ListPastSocialView):
    template_name = 'events/bedpres/list_past.html'
    model = Bedpres


class ListSocialDeleteView(PermissionRequiredMixin, ListView):
    template_name = 'events/social/delete.html'
    permission_required = 'events.delete_event'
    model = Social

    def queryset(self):
        return self.model.objects.filter(date__gt=timezone.now(),
                                         published=True)


class ListBedpresDeleteView(ListSocialDeleteView):
    template_name = 'events/bedpres/delete.html'
    model = Bedpres
    permission_required = 'events.delete_bedpres'


class DeleteSocialView(PermissionRequiredMixin, DeleteView):
    model = Social
    permission_required = 'events.delete_event'
    success_url = reverse_lazy('events:delete_list_social')

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.published = False
        object.save()
        messages.add_message(request, messages.WARNING, 'Arrangementet ble slettet', extra_tags='Slettet')
        return HttpResponseRedirect(self.success_url)


class DeleteBedpresView(DeleteSocialView):
    model = Bedpres
    success_url = reverse_lazy('events:delete_list_bedpres')
    permission_required = 'events.delete_bedpres'


class ViewSocialDetailsView(DetailView):
    template_name = 'events/social/detail.html'
    model = Social

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        Registration = self.model.attendees.through
        attendees = Registration.objects. \
            prefetch_related('user__profile'). \
            order_by('user__profile__grade', 'user__first_name')

        confirmed = attendees.filter(event=self.object, status=REGISTRATION_STATUS.CONFIRMED)
        waiting = attendees.filter(event=self.object, status=REGISTRATION_STATUS.WAITING)
        context.update({'attendees': confirmed, 'waiting_list': waiting})
        return context


class ViewBedpresDetailsView(ViewSocialDetailsView):
    template_name = 'events/bedpres/detail.html'
    model = Bedpres


class SocialEditRemoveUserRegistration(SingleObjectMixin, MultiFormsView):
    model = Social
    registration_model = EventRegistration
    template_name = 'events/social/deregister_or_edit.html'
    form_classes = {'deregister': DeRegisterUserForm,
                    'edit': SocialRegisterUserForm}
    success_url = 'event:register'
    email_template = 'social'

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
        # Todo: Make it possible to remove registration whenever, IF it is of "interest" type

        # Remove the forms whenever the deadline has passed
        if not self.object.can_de_register:
            context.pop('deregister')
            if context.get('edit'):
                context.pop('edit')

        # Add queue position
        registration = self.registration
        if registration:
            if registration.status == REGISTRATION_STATUS.WAITING:
                queue_position = self.registration_model.objects.filter(event=registration.event,
                                                                        created__lt=registration.created,
                                                                        status=REGISTRATION_STATUS.WAITING).count() + 1
                context.update({'queue_position': queue_position})

        context['registration'] = registration
        return context

    def deregister_form_valid(self, form):
        event = self.object

        # Deregister the current user and give a slot to the first user in the event queue
        if event.can_de_register:
            registration = self.registration_model.objects.filter(event=event, user=self.request.user).first()
            lucky_person = self.registration_model.objects.de_register(registration)
            if lucky_person:
                send_event_mail(lucky_person, event, self.email_template)
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
    email_template = 'bedpres'

    def get_edit_initial(self):
        return {'instance': self.registration}


class SocialRegisterUserView(SingleObjectMixin, View):
    template_name = "events/register_user.html"
    model = Social

    registration_form = SocialRegisterUserForm
    email_template = 'social'

    pk = None
    object = None

    def get_success_url(self):
        return reverse('events:register_social', kwargs={'pk': self.pk})

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
            "allowed_grade": self.object.allowed_grade(request.user)
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
            return redirect(self.get_success_url())
        context = {
            'registration_form': registration_form,
            'event': event,
        }
        return render(request, self.template_name, context)

    def set_status_message(self, request, status, instance, event):
        if status == REGISTRATION_STATUS.CONFIRMED:
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Du er påmeldt arrangementet.',
                                 extra_tags='Påmeldt')

            custom_messages = RegistrationMessage.objects.filter(user=instance.user, event=event)
            for custom_message in custom_messages:
                messages.add_message(request,
                                     messages.INFO,
                                     custom_message.message,
                                     extra_tags='PS')

        elif status == REGISTRATION_STATUS.WAITING:
            messages.add_message(request,
                                 messages.WARNING,
                                 'Arrangementet er fullt, men du er på venteliste.',
                                 extra_tags='Venteliste')

        elif status == REGISTRATION_STATUS.INTERESTED:
            messages.add_message(request,
                                 messages.INFO,
                                 'Det er ikke åpent for ditt klassetrinn, men vi har notert din interesse. '
                                 'Du blir påmeldt automatisk og tilsendt en e-post dersom dette endres.',
                                 extra_tags='Interessert')

        send_event_mail(instance, event, self.email_template)


class BedpresRegisterUserView(SocialRegisterUserView):
    template_name = 'events/register_user.html'
    model = Bedpres
    email_template = 'bedpres'

    registration_form = BedpresRegisterUserForm

    def get_form_kwargs(self):
        return {}


class SocialBaseRegisterUserView(LoginRequiredMixin, SingleObjectMixin, View):
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


class SocialEnlistedUsersView(PermissionRequiredMixin, DetailView, View):
    template_name = 'events/admin_list.html'
    model = Social
    registration_model = EventRegistration
    permission_required = 'event.change_eventregistration'

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
    permission_required = 'event.change_bedpresregistration'


@login_required
@permission_required('events.change_eventregistration')
def change_payment_status(request, registration_id):
    registration = EventRegistration.objects.get(pk=registration_id)
    registration.payment_status = not registration.payment_status
    registration.save()
    return JsonResponse({'payment_status': registration.payment_status})


@transaction.atomic
def set_user_event_status(event, registration):
    if event.allowed_grade(registration.user):
        if event.has_spare_slots:
            registration.confirm()
            registration.save()
            return REGISTRATION_STATUS.CONFIRMED
        else:
            registration.waiting()
            return REGISTRATION_STATUS.WAITING
    else:
        return REGISTRATION_STATUS.INTERESTED
