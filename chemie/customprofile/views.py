from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .email import send_forgot_password_mail
from .forms import RegisterUserForm, RegisterProfileForm, EditUserForm, EditProfileForm, ForgotPassword, SetNewPassword, LifeTimeMember
from .models import UserToken, Profile, Membership


def register_user(request):
    user_core_form = RegisterUserForm(request.POST or None)
    user_profile_form = RegisterProfileForm(request.POST or None)
    if user_core_form.is_valid() and user_profile_form.is_valid():
        user = user_core_form.save(commit=False)
        user.set_password(user_core_form.password_matches())
        user.save()

        profile = user_profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.add_message(request, messages.SUCCESS, 'Brukeren din er opprettet!', extra_tags='Takk!')
        return HttpResponseRedirect('/')
    context = {
        "user_core_form": user_core_form,
        "user_profile_form": user_profile_form,
    }
    return render(request, 'userregistration/register.html', context)

@login_required
def edit_profile(request):
    user = request.user
    new_password_form = PasswordChangeForm(user=user, data=request.POST or None)
    user_form = EditUserForm(request.POST or None, instance=request.user)
    profile_form = EditProfileForm(request.POST or None, instance=request.user.profile)
    if request.POST:
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if not new_password_form.has_changed():
                # har ikke fyllt inn noen felter i passord formen
                new_password_form = PasswordChangeForm(user=user, data=None)
                messages.add_message(request, messages.SUCCESS, 'Bra jobba! Dine endringer er lagret!', extra_tags='OBS! Sarkastisk melding')
                return HttpResponseRedirect('/')
            else:
                # brukeren har fyllt inn minst ett felt i passord formen
                if new_password_form.is_valid():
                    new_password_form.save()
                    update_session_auth_hash(request, new_password_form.user)
                    messages.add_message(request, messages.SUCCESS, 'Passordet ble endret', extra_tags='Suksess')
                    return HttpResponseRedirect('/')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        'change_password_form': new_password_form,
    }
    return render(request, 'userregistration/editprofile.html', context)

@login_required
def change_password(request):
    user = request.user
    new_password_form = PasswordChangeForm(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)

    context = {
        'change_password_form': new_password_form,
    }
    return render(request, 'userregistration/changepassword.html', context)


def forgot_password(request):
    form = ForgotPassword(request.POST or None)
    if request.POST:
        email = form.data.get('email')
        if form.is_valid():
            user = User.objects.get(email=email)
            if user:
                token = UserToken.objects.create(user=user)
                send_forgot_password_mail(request, email, user, token)
                HttpResponseRedirect('/')
    context = {
        'email': form,
    }
    return render(request, 'userregistration/forgot_password.html', context)


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
            return HttpResponseRedirect('/')

    context = {
        'form': password_form,
    }
    return render(request, 'userregistration/setforgottenpassword.html', context)

def change_membership_status(request, id):
    person = User.objects.get(pk=id).profile
    person.membership = Membership(
        start_date = timezone.now(),
        end_date = timezone.now() + timedelta(365*5),
        endorser = request.user
        )
    person.membership.save()
    person.save()
    membership_status = person.membership.is_active()
    return JsonResponse({'membership_status': membership_status})

def manage_memberships(request):
    form = LifeTimeMember(request.POST or None)
    if request.POST:
        if request.is_ajax():
            change_membership_status(request)
    users = Profile.objects.all()
    context = {
        "users": users,
        "form": form,
    }
    return render(request, "userregistration/memberships.html", context)
