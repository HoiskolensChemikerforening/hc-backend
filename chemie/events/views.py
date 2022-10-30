from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
)
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import (
    CreateView,
    FormView,
    DeleteView,
    UpdateView,
)

# from django.forms import modelformset_factory
from django.views.generic.list import ListView
from django.db.models import Q

from chemie.customprofile.forms import GetRFIDForm
from chemie.customprofile.models import ProfileManager, Profile, User, GRADES
from .email import send_event_mail
from .extras import MultiFormsView
from .forms import (
    RegisterEventForm,
    SocialRegisterUserForm,
    DeRegisterUserForm,
    RegisterBedpresForm,
    BedpresRegisterUserForm,
)

from .models import (
    Social,
    SocialEventRegistration,
    REGISTRATION_STATUS,
    RegistrationMessage,
    Bedpres,
    BedpresRegistration,
    ARRIVAL_STATUS,
)

from rest_framework import generics

from .serializer import (
    SocialSerializer,
    SocialEventRegistrationSerializer,
    BedpresSerializer,
    BedpresRegistrationSerializer,
)


class SuccessMessageMixin(object):
    message_content = "", "", ""

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        message_type, message, heading = self.message_content
        messages.add_message(
            self.request, message_type, message, extra_tags=heading
        )
        return response


class SocialFormView(FormView):
    template_name = "events/social/create.html"
    form_class = RegisterEventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    class Meta:
        abstract = True


class CreateSocialView(
    PermissionRequiredMixin, SuccessMessageMixin, SocialFormView, CreateView
):
    success_url = reverse_lazy("events:index_social")
    permission_required = "events.add_social"
    # TODO: Couple the allowed grades with GRADES enum
    # from customprofile models
    initial = {"allowed_grades": list(GRADES.values.keys())}
    success_message = "%(name)s was created successfully"
    message_content = (
        messages.SUCCESS,
        "Arrangementet ble opprettet",
        "Opprettet",
    )


class EditSocialView(
    PermissionRequiredMixin, SuccessMessageMixin, SocialFormView, UpdateView
):
    permission_required = "events.change_social"
    # Can't edit past events
    queryset = Social.objects.filter(date__gte=timezone.now())
    success_message = "%(name)s was created successfully"
    message_content = messages.SUCCESS, "Arrangementet ble endret", "Endret"


class BedpresFormView(SocialFormView):
    template_name = "events/bedpres/create.html"
    form_class = RegisterBedpresForm


class CreateBedpresView(
    PermissionRequiredMixin, SuccessMessageMixin, BedpresFormView, CreateView
):
    success_url = reverse_lazy("events:index_bedpres")
    permission_required = "events.add_bedpres"
    # TODO: Couple the allowed grades with GRADES enum
    # from customprofile models
    initial = {"allowed_grades": list(GRADES.values.keys())}
    message_content = messages.SUCCESS, "Bedpresen ble opprettet", "Opprettet"


class EditBedpresView(
    PermissionRequiredMixin, SuccessMessageMixin, BedpresFormView, UpdateView
):
    permission_required = "events.change_bedpres"
    # Can't edit past events
    queryset = Bedpres.objects.filter(date__gte=timezone.now())
    message_content = messages.SUCCESS, "Bedpresen ble endret", "Endret"


class ListSocialView(ListView):
    template_name = "events/social/list.html"
    model = Social

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        future_events = self.model.objects.filter(
            date__gt=timezone.now(), published=True
        ).order_by("date")

        my_events = None
        if self.request.user.is_authenticated:
            attending_events = Q(attendees__username__exact=self.request.user)
            authored_events = Q(author=self.request.user)
            my_events = self.model.objects.filter(
                attending_events | authored_events
            ).distinct()

        context.update({"events": future_events, "my_events": my_events})
        return context


class ListBedpresView(ListSocialView):
    template_name = "events/bedpres/list.html"
    model = Bedpres


class ListPastSocialView(ListView):
    template_name = "events/social/list_past.html"
    model = Social

    def queryset(self):
        return self.model.objects.filter(date__lte=timezone.now()).order_by(
            "-date"
        )


class ListPastBedpresView(ListPastSocialView):
    template_name = "events/bedpres/list_past.html"
    model = Bedpres


class ListSocialDeleteView(PermissionRequiredMixin, ListView):
    template_name = "events/social/delete.html"
    permission_required = "events.delete_social"
    model = Social

    def queryset(self):
        return self.model.objects.filter(
            date__gt=timezone.now(), published=True
        )


class ListBedpresDeleteView(ListSocialDeleteView):
    template_name = "events/bedpres/delete.html"
    model = Bedpres
    permission_required = "events.delete_bedpres"


class DeleteSocialView(PermissionRequiredMixin, DeleteView):
    model = Social
    permission_required = "events.delete_social"
    success_url = reverse_lazy("events:delete_list_social")

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.published = False
        object.save()
        messages.add_message(
            request,
            messages.WARNING,
            "Arrangementet ble slettet",
            extra_tags="Slettet",
        )
        return HttpResponseRedirect(self.success_url)


class DeleteBedpresView(DeleteSocialView):
    model = Bedpres
    success_url = reverse_lazy("events:delete_list_bedpres")
    permission_required = "events.delete_bedpres"


class ViewSocialDetailsView(DetailView):
    template_name = "events/social/detail.html"
    model = Social
    registration_model = SocialEventRegistration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        Registration = self.model.attendees.through
        attendees = Registration.objects.prefetch_related(
            "user__profile"
        ).order_by("user__profile__grade", "user__first_name")

        confirmed = attendees.filter(
            event=self.object, status=REGISTRATION_STATUS.CONFIRMED
        )

        waiting = attendees.filter(
            event=self.object, status=REGISTRATION_STATUS.WAITING
        ).order_by("created")

        context.update({"attendees": confirmed, "waiting_list": waiting})
        return context


class ViewBedpresDetailsView(ViewSocialDetailsView):
    template_name = "events/bedpres/detail.html"
    model = Bedpres


class SocialEditRemoveUserRegistration(
    LoginRequiredMixin, SingleObjectMixin, MultiFormsView
):
    model = Social
    registration_model = SocialEventRegistration
    template_name = "events/social/deregister_or_edit.html"
    form_classes = {
        "deregister": DeRegisterUserForm,
        "edit": SocialRegisterUserForm,
    }
    success_url = "event:register"
    email_template = "social"

    registration = None
    object = None

    def get_edit_initial(self):
        # The boolean fields must be passed to the form along with
        # any instance of current model
        return {
            "enable_sleepover": self.object.sleepover,
            "enable_night_snack": self.object.night_snack,
            "enable_companion": self.object.companion,
            "instance": self.registration,
        }

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object.
        # This is run very early
        self.object = self.get_object()
        self.registration = self.registration_model.objects.filter(
            event=self.object, user=self.request.user
        ).first()
        return super().dispatch(request)

    def get_object(self, queryset=None):
        obj = self.kwargs.get("object")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(super().get_context_data(**kwargs))
        # Todo: Make it possible to remove registration whenever,
        # IF it is of "interest" type

        # Remove the forms whenever the deadline has passed
        if not self.object.can_de_register:
            context["forms"].pop("deregister")
            if context["forms"].get("edit"):
                context["forms"].pop("edit")

        # Remove edit forms if none of the fields are present
        edit_form_boolean = (
            self.object.companion
            or self.object.sleepover
            or self.object.night_snack
        )
        # Remove edit if no fields and editform is in context
        if not (edit_form_boolean) and context["forms"].get("edit"):
            context["forms"].pop("edit")

        # Add queue position
        registration = self.registration
        if registration:
            if registration.status == REGISTRATION_STATUS.WAITING:
                queue_position = (
                    self.registration_model.objects.filter(
                        event=registration.event,
                        created__lt=registration.created,
                        status=REGISTRATION_STATUS.WAITING,
                    ).count()
                    + 1
                )
                context.update({"queue_position": queue_position})
        context["registration"] = registration
        return context

    def deregister_form_valid(self, form):
        event = self.object

        # Deregister the current user and give a slot
        # to the first user in the event queue
        if event.can_de_register:
            registration = self.registration_model.objects.filter(
                event=event, user=self.request.user
            ).first()
            lucky_person = self.registration_model.objects.de_register(
                registration
            )
            if lucky_person:
                send_event_mail(lucky_person, event, self.email_template)
            messages.add_message(
                self.request,
                messages.WARNING,
                "Du er nå avmeldt {}".format(event.title),
                extra_tags="Avmeldt",
            )
        return redirect(event.get_absolute_registration_url())

    def edit_form_valid(self, form):
        # Form fields must be set as None is not a valid option
        registration = self.registration
        registration.night_snack = form.cleaned_data.get("night_snack") or 0
        registration.sleepover = form.cleaned_data.get("sleepover") or 0
        registration.companion = form.cleaned_data.get("companion")
        registration.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Påmeldingsdetaljene ble endret",
            extra_tags="Endringer utført",
        )

        return redirect(registration.event.get_absolute_registration_url())

    def signup_form_valid(self, form):
        user = form.save(self.request)
        return form.signup(self.request, user, self.get_success_url())


class BedpresEditRemoveUserRegistration(
    LoginRequiredMixin, SingleObjectMixin, MultiFormsView
):
    model = Bedpres
    registration_model = BedpresRegistration
    template_name = "events/bedpres/deregister_or_edit.html"
    form_classes = {"deregister": DeRegisterUserForm}
    email_template = "bedpres"

    def get_edit_initial(self):
        return {"instance": self.registration}

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object.
        # This is run very early
        self.object = self.get_object()
        self.registration = self.registration_model.objects.filter(
            event=self.object, user=self.request.user
        ).first()
        return super().dispatch(request)

    def get_object(self, queryset=None):
        obj = self.kwargs.get("object")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(super().get_context_data(**kwargs))
        # Todo: Make it possible to remove registration whenever,
        # IF it is of "interest" type

        # Remove the forms whenever the deadline has passed
        if not self.object.can_de_register:
            context["forms"].pop("deregister")
            if context["forms"].get("edit"):
                context["forms"].pop("edit")

        # Remove edit if no fields and editform is in context
        if context["forms"].get("edit"):
            context["forms"].pop("edit")

        # Add queue position
        registration = self.registration
        if registration:
            if registration.status == REGISTRATION_STATUS.WAITING:
                queue_position = (
                    self.registration_model.objects.filter(
                        event=registration.event,
                        created__lt=registration.created,
                        status=REGISTRATION_STATUS.WAITING,
                    ).count()
                    + 1
                )
                context.update({"queue_position": queue_position})

        context["registration"] = registration
        return context

    def deregister_form_valid(self, form):
        event = self.object

        # Deregister the current user and give a slot
        # to the first user in the event queue
        if event.can_de_register:
            registration = self.registration_model.objects.filter(
                event=event, user=self.request.user
            ).first()
            lucky_person = self.registration_model.objects.de_register(
                registration
            )
            if lucky_person:
                send_event_mail(lucky_person, event, self.email_template)
            messages.add_message(
                self.request,
                messages.WARNING,
                "Du er nå avmeldt {}".format(event.title),
                extra_tags="Avmeldt",
            )
        return redirect(event.get_absolute_registration_url())

    def edit_form_valid(self, form):
        # Form fields must be set as None is not a valid option
        registration = self.registration
        registration.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Påmeldingsdetaljene ble endret",
            extra_tags="Endringer utført",
        )

        return redirect(registration.event.get_absolute_registration_url())

    def signup_form_valid(self, form):
        user = form.save(self.request)
        return form.signup(self.request, user, self.get_success_url())


class SocialRegisterUserView(LoginRequiredMixin, SingleObjectMixin, View):
    template_name = "events/register_user.html"
    model = Social

    registration_form = SocialRegisterUserForm
    email_template = "social"

    pk = None
    object = None

    @staticmethod
    @transaction.atomic
    def set_user_event_status(event, registration):
        if event.allowed_grade(registration.user):
            slots = event.sluts - event.registered_users()
            has_spare_slots = slots > 0
            if has_spare_slots:
                registration.confirm()
                registration.save()
                return REGISTRATION_STATUS.CONFIRMED
            else:
                registration.waiting()
                return REGISTRATION_STATUS.WAITING
        else:
            return REGISTRATION_STATUS.INTERESTED

    def get_success_url(self):
        return reverse("events:register_social", kwargs={"pk": self.pk})

    def dispatch(self, request, *args, **kwargs):
        # Set event and registration on the whole object
        # This is run very early
        self.object = self.get_object()
        return super().dispatch(request, self.pk)

    def get_object(self, queryset=None):
        self.pk = self.kwargs.get("pk")
        return self.model.objects.get(pk=self.pk)

    def get_form_kwargs(self):
        return {
            "enable_sleepover": self.object.sleepover,
            "enable_night_snack": self.object.night_snack,
            "enable_companion": self.object.companion,
        }

    def get(self, request, pk, *args, **kwargs):
        if self.object.can_signup:
            registration_form = self.registration_form(
                **self.get_form_kwargs()
            )
        else:
            registration_form = None
        context = {
            "registration_form": registration_form,
            "event": self.object,
            "allowed_grade": self.object.allowed_grade(request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        self.object = get_object_or_404(self.model, pk=pk)
        registration_form = self.registration_form(
            request.POST, **self.get_form_kwargs()
        )
        event = self.object
        self.pk = pk
        if registration_form.is_valid():
            instance = registration_form.save(commit=False)
            instance.event = self.object
            instance.user = request.user
            instance.save()
            status = self.set_user_event_status(event, instance)
            self.set_status_message(request, status, instance, event)
            return redirect(self.get_success_url())
        context = {
            "registration_form": registration_form,
            "event": self.object,
            "allowed_grade": self.object.allowed_grade(request.user),
        }
        return render(request, self.template_name, context)

    def set_status_message(self, request, status, instance, event):
        if status == REGISTRATION_STATUS.CONFIRMED:
            messages.add_message(
                request,
                messages.SUCCESS,
                "Du er påmeldt arrangementet.",
                extra_tags="Påmeldt",
            )

            custom_messages = event.custom_message.filter(user=instance.user)

            for custom_message in custom_messages:
                messages.add_message(
                    request,
                    messages.INFO,
                    custom_message.message,
                    extra_tags="PS",
                )

        elif status == REGISTRATION_STATUS.WAITING:
            messages.add_message(
                request,
                messages.WARNING,
                "Arrangementet er fullt, men du er på venteliste.",
                extra_tags="Venteliste",
            )

        elif status == REGISTRATION_STATUS.INTERESTED:
            # TODO: Fix the klassetrinn message. Could be error due to specialization
            messages.add_message(
                request,
                messages.INFO,
                "Det er ikke åpent for ditt klassetrinn, "
                "men vi har notert din interesse. Du blir påmeldt "
                "automatisk og tilsendt en e-post dersom dette endres.",
                extra_tags="Interessert",
            )
        send_event_mail(instance, event, self.email_template)


class BedpresRegisterUserView(SocialRegisterUserView):
    template_name = "events/register_user.html"
    model = Bedpres
    email_template = "bedpres"

    registration_form = BedpresRegisterUserForm

    @staticmethod
    @transaction.atomic
    def set_user_event_status(event, registration):
..        if event.allowed_grade(registration.user) and event.allowed_specialization(registration.user):
            slots = event.sluts - event.registered_users()
            has_spare_slots = slots > 0
            if has_spare_slots:
                registration.confirm()
                registration.save()
                return REGISTRATION_STATUS.CONFIRMED
            else:
                registration.waiting()
                return REGISTRATION_STATUS.WAITING
        else:
            return REGISTRATION_STATUS.INTERESTED

    def get_success_url(self):
        return reverse("events:register_bedpres", kwargs={"pk": self.pk})

    def get_form_kwargs(self):
        return {}

    def get_success_url(self):
        return reverse("events:register_bedpres", kwargs={"pk": self.pk})


class SocialBaseRegisterUserView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Social
    registration_model = SocialEventRegistration
    registration_view_edit = SocialEditRemoveUserRegistration
    registration_view_register = SocialRegisterUserView

    def set_initial(self):
        # Set event and registration on the whole object
        # This is run very early
        self.object = self.get_object()
        self.registration = self.registration_model.objects.filter(
            event=self.object, user=self.request.user
        ).first()

    def get(self, request, pk):
        # Fetch event object
        self.set_initial()
        event = self.object
        registration = self.registration_model.objects.filter(
            event=event, user=request.user
        ).first()

        if registration:
            return self.registration_view_edit.as_view()(
                self.request, object=event, registration=registration
            )
        else:
            if request.method == "POST":
                return self.registration_view_register.post(
                    self.registration_view_register(), request, self.object.pk
                )
            else:
                return self.registration_view_register.as_view()(
                    self.request, event, pk=pk
                )

    def post(self, request, pk):
        self.set_initial()
        return self.get(request, pk)


class BedpresBaseRegisterUserView(SocialBaseRegisterUserView):
    model = Bedpres
    registration_model = BedpresRegistration
    registration_view_edit = BedpresEditRemoveUserRegistration
    registration_view_register = BedpresRegisterUserView

    def get(self, request, pk):
        # Fetch event object
        self.set_initial()
        event = self.object
        registration = self.registration_model.objects.filter(
            event=event, user=request.user
        ).first()

        if registration:
            return self.registration_view_edit.as_view()(
                self.request, object=event, registration=registration
            )
        else:
            if request.method == "POST":
                return self.registration_view_register.post(
                    self.registration_view_register(), request, self.object.pk
                )
            else:
                return self.registration_view_register.as_view()(
                    self.request, event, pk=pk
                )


class SocialEnlistedUsersView(PermissionRequiredMixin, DetailView, View):
    template_name = "events/admin_list.html"
    model = Social
    registration_model = SocialEventRegistration
    permission_required = "events.change_socialeventregistration"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context["event"] = self.object
            context["attendees"] = self.registration_model.objects.filter(
                status=REGISTRATION_STATUS.CONFIRMED, event=self.object
            ).select_related("user__profile__membership")
            paid = self.registration_model.objects.filter(
                status=REGISTRATION_STATUS.CONFIRMED,
                event=self.object,
                payment_status=True,
            ).count()
            not_paid = self.registration_model.objects.filter(
                status=REGISTRATION_STATUS.CONFIRMED,
                event=self.object,
                payment_status=False,
            ).count()
            try:
                context["percentage_paid"] = round(
                    (paid // (not_paid + paid)) * 100
                )
            except ZeroDivisionError:
                context["percentage_paid"] = 0
            context["total_paid"] = paid
            context["total_not_paid"] = not_paid
            context["is_bedpres"] = False
            context["social_has_checkin"] = self.object.check_in
        return context


class BedpresEnlistedUsersView(PermissionRequiredMixin, DetailView, View):
    template_name = "events/admin_list.html"
    model = Bedpres
    registration_model = BedpresRegistration
    permission_required = "events.change_bedpresregistration"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context["attendees"] = self.registration_model.objects.filter(
                status=REGISTRATION_STATUS.CONFIRMED, event=self.object
            ).select_related("user__profile__membership")
        context["is_bedpres"] = True
        return context


@login_required
@permission_required("events.change_socialeventregistration")
def change_payment_status(request):
    if request.method == "POST":
        registration_id = request.POST["registration_id"]
        registration = SocialEventRegistration.objects.get(pk=registration_id)
        registration.payment_status = not registration.payment_status
        registration.save()
        return JsonResponse({"payment_status": registration.payment_status})
    else:
        return redirect(reverse("home:home"))


@login_required
@permission_required(
    "events.change_bedpresregistration"
    or "events.change_socialeventregistration"
)
def change_arrival_status(request):
    if request.method == "POST":
        registration_id = request.POST["registration_id"]
        if "bedpres" in request.path:
            registration = BedpresRegistration.objects.get(pk=registration_id)
        else:
            registration = SocialEventRegistration.objects.get(
                pk=registration_id
            )
        status = registration.arrival_status
        if status == ARRIVAL_STATUS.NONE or status == ARRIVAL_STATUS.TRUANT:
            registration.arrival_status = ARRIVAL_STATUS.PRESENT
            registration.save()
            return JsonResponse({"arrival_status": 1})
        else:
            # status is neither 'not set' nor 'not met' => status is 'met'
            registration.arrival_status = ARRIVAL_STATUS.TRUANT
            registration.save()
            return JsonResponse({"arrival_status": 0})
    else:
        return redirect(reverse("home:home"))


@permission_required("events.change_bedpresregistration")
@login_required
def checkin_to_bedpres(request, pk):
    form = GetRFIDForm(request.POST or None)
    bedpres = Bedpres.objects.get(pk=pk)
    if request.method == "POST":
        if form.is_valid():
            rfid = form.cleaned_data.get("rfid")
            em_code = ProfileManager.rfid_to_em(rfid)
            try:
                user = Profile.objects.get(access_card=em_code).user
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Studentkortnummeret er ikke registrert enda.",
                )
                return redirect(
                    f"{reverse('profile:add_rfid')}?cardnr={rfid}&redirect={request.get_full_path()}"
                )
            try:
                registration = BedpresRegistration.objects.get(
                    user=user, event=bedpres
                )
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} er ikke påmeldt {}".format(
                        user.get_full_name(), bedpres.title
                    ),
                )
                return redirect(
                    reverse("events:checkin_bedpres", kwargs={"pk": pk})
                )
            if registration.status == REGISTRATION_STATUS.CONFIRMED:
                registration.arrival_status = ARRIVAL_STATUS.PRESENT
                registration.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "{} har sjekket inn på {}".format(
                        user.get_full_name(), registration.event.title
                    ),
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} står enda på venteliste. Sjekk inn manuelt.".format(
                        user.get_full_name()
                    ),
                )
            return redirect(
                reverse("events:checkin_bedpres", kwargs={"pk": pk})
            )
    context = {"form": form, "bedpres": bedpres}
    return render(request, "events/bedpres/check_in.html", context)


@permission_required("events.change_socialeventregistration")
@login_required
def check_in_to_social(request, pk):
    form = GetRFIDForm(request.POST or None)
    social = Social.objects.get(id=pk)
    if request.method == "POST":
        if form.is_valid():
            rfid = form.cleaned_data.get("rfid")
            em_code = ProfileManager.rfid_to_em(rfid)
            try:
                user = Profile.objects.get(access_card=em_code).user
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Studentkortnummeret er ikke registrert enda.",
                )
                return redirect(
                    f"{reverse('profile:add_rfid')}?cardnr={rfid}&redirect={request.get_full_path()}"
                )
            try:
                registration = SocialEventRegistration.objects.get(
                    user=user, event=social
                )
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} er ikke påmeldt {}".format(
                        user.get_full_name(), social.title
                    ),
                )
                return redirect(
                    reverse("events:checkin_social", kwargs={"pk": pk})
                )
            if registration.status == REGISTRATION_STATUS.CONFIRMED:
                registration.arrival_status = ARRIVAL_STATUS.PRESENT
                registration.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "{} har sjekket inn på {}".format(
                        user.get_full_name(), registration.event.title
                    ),
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} står enda på venteliste. Sjekk inn manuelt.".format(
                        user.get_full_name()
                    ),
                )
            return redirect(
                reverse("events:checkin_social", kwargs={"pk": pk})
            )
    context = {"form": form, "social": social}
    return render(request, "events/social/check_in.html", context)


class SocialListCreate(generics.ListCreateAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialSerializer


class SocialEventRegistrationListCreate(generics.ListCreateAPIView):
    queryset = SocialEventRegistration.objects.all()
    serializer_class = SocialEventRegistrationSerializer


class BedpresListCreate(generics.ListCreateAPIView):
    queryset = Bedpres.objects.all()
    serializer_class = BedpresSerializer


class BedpresRegistrationListCreate(generics.ListCreateAPIView):
    queryset = BedpresRegistration.objects.all()
    serializer_class = BedpresRegistrationSerializer


class SocialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Social.objects.all()
    serializer_class = SocialSerializer


class SocialEventRegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialEventRegistration.objects.all()
    serializer_class = SocialEventRegistrationSerializer


class BedpresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bedpres.objects.all()
    serializer_class = BedpresSerializer


class BedpresRegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BedpresRegistration.objects.all()
    serializer_class = BedpresRegistrationSerializer
