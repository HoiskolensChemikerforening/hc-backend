from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (LoginView as OldLoginView, SuccessURLAllowedHostsMixin)
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import FormView

from .email import send_forgot_password_mail
from .forms import RegisterUserForm, RegisterProfileForm, EditUserForm, EditProfileForm, ForgotPassword, \
    SetNewPassword, NameSearchForm
from .models import UserToken, Profile, Membership, GRADES
from django.contrib.auth.forms import AuthenticationForm
from .forms import ApprovedTermsForm

def register_user(request):
    user_core_form = RegisterUserForm(request.POST or None)
    user_profile_form = RegisterProfileForm(request.POST or None, request.FILES or None)
    if user_core_form.is_valid() and user_profile_form.is_valid():
        user = user_core_form.save(commit=False)
        user.set_password(user_core_form.password_matches())
        user.save()

        profile = user_profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.add_message(request, messages.SUCCESS, 'Brukeren din er opprettet!', extra_tags='Takk!')
        return redirect('profile:register')
    context = {
        "user_core_form": user_core_form,
        "user_profile_form": user_profile_form,
    }
    return render(request, 'customprofile/register.html', context)


@login_required
def edit_profile(request):
    user = request.user
    new_password_form = PasswordChangeForm(user=user, data=request.POST or None)
    user_form = EditUserForm(request.POST or None, instance=request.user)
    try:
        current_profile = request.user.profile
    except:
        current_profile = Profile(user=user)
    profile_form = EditProfileForm(request.POST or None, instance=current_profile)
    if request.POST:
        if new_password_form.has_changed():
            # The user has filled in something in at least one field
            if new_password_form.is_valid():
                new_password_form.save()
                update_session_auth_hash(request, new_password_form.user)
                new_password_form = PasswordChangeForm(user=user, data=None)
        else:
            # Reset the password form because of the errors it throws, being empty raises errors
            new_password_form = PasswordChangeForm(user=user)
        if user_form.has_changed() or profile_form.has_changed():
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

        if not (user_form.errors or profile_form.errors or new_password_form.errors):
            messages.add_message(request, messages.SUCCESS, 'Dine endringer har blitt lagret!')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        'change_password_form': new_password_form,
    }
    return render(request, 'customprofile/editprofile.html', context)


def forgot_password(request):
    form = ForgotPassword(request.POST or None)
    if request.POST:
        email = form.data.get('email')
        if form.is_valid():
            try:
                user = User.objects.get(email=email)
                token = UserToken.objects.create(user=user)
                send_forgot_password_mail(email, user, token)
                messages.add_message(request, messages.SUCCESS, 'Sjekk {} for videre detaljer'.format(email),
                                     extra_tags='Tilbakestille passord')
                return redirect(reverse('frontpage:home'))

            except ObjectDoesNotExist:
                form.add_error(None, ValidationError(
                    {'email': ["Vi finner ingen bruker med denne e-posten"]}))

    context = {
        'form': form,
    }
    return render(request, 'customprofile/forgot_password.html', context)


def activate_password(request, code):
    try:
        activator = UserToken.objects.get(key=code)
    except ObjectDoesNotExist:
        raise Http404
    password_form = SetNewPassword(request.POST or None)
    if request.POST:
        if password_form.is_valid():
            password = password_form.data.get('password_new')
            activator.set_password(password)
            messages.add_message(request, messages.SUCCESS, 'Ditt passord ble endret', extra_tags='Suksess')
            return redirect(reverse('frontpage:home'))

    context = {
        'form': password_form,
    }
    return render(request, 'customprofile/set_forgotten_password.html', context)


@permission_required('customprofile.change_membership')
def view_memberships(request):
    profiles = Profile.objects.all().select_related('user', 'membership')
    context = {
        "profiles": profiles,
    }
    return render(request, "customprofile/memberships.html", context)


@permission_required('customprofile.change_membership')
def change_membership_status(request, profile_id):
    person = Profile.objects.get(pk=profile_id)
    if person.membership is None:
        membership = Membership(
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(365*5),
            endorser=request.user
            )
        membership.save()
        person.membership = membership
        person.save()
    membership_status = person.membership.is_active()
    return JsonResponse({'membership_status': membership_status})


@login_required
def yearbook(request, year=1):
    year = int(year)
    # If url arg year is invalid, make it valid.
    if year not in GRADES:
        if year > GRADES.FIFTH.value:
            year = GRADES.FIFTH.value
        else:
            year = 1
    form = NameSearchForm(request.POST or None)
    profiles = Profile.objects.none()
    if request.method == 'POST':
        if form.is_valid():
            search_field = form.cleaned_data.get('search_field')
            users = find_user_by_name(search_field)
            profiles = Profile.objects.filter(user__in=users)
    else:
        profiles = Profile.objects.filter(grade=year, user__is_active=True).order_by('user__last_name')
    context = {
        'profiles': profiles,
        'grades': GRADES,
        'search_form': form,
    }
    return render(request, 'customprofile/yearbook.html', context)


def find_user_by_name(query_name):
    qs = User.objects.all()
    for term in query_name.split():
        qs = qs.filter( Q(first_name__icontains=term) | Q(last_name__icontains=term))
    return qs


class LoginView(OldLoginView):
    # Få denne til å redirecte til det udner

    def form_valid(self, form):
        user = form.get_user()
        if user.profile.approved_terms:
            return super().form_valid(form)

        self.approval_form_view(self.request, form)

    def approval_form_view(self, request, loginform):
        if request.method == 'POST':
            if loginform.is_valid():
                termsform = ApprovedTermsForm(request.POST)
                user = loginform.get_user()
                approval = termsform['approval'].value()
                if approval:
                    user.profile.approved_terms = True

                super().form_valid(loginform)
        else:
            termsform = ApprovedTermsForm()
            return render(request, 'login.html', {'form': loginform, 'termsform': termsform})

        """
        Display the login form and a "consent" form.
        If the user login is correct and consent is given: set value and
        redirect to home page
        """