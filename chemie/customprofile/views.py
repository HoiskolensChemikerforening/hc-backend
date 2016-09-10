from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegisterUserForm, RegisterProfileForm, EditUserForm, EditProfileForm


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