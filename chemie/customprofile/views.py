from django.shortcuts import render, get_object_or_404
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import RegisterUserForm, RegisterProfileForm, EditUserForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


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
        context = {
            "title": 'Fullført',
            "message": 'Registreringen ble fullført!',
            "status": 'success',
        }
        return render(request, 'common/feedback.html', context)

    context = {
        "user_core_form": user_core_form,
        "user_profile_form": user_profile_form,
    }
    return render(request, 'userregistration/register.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Dine endringer er lagret, Stormführer.', extra_tags='Sieg Heil')
        else:
            messages.add_message(request, messages.ERROR, 'Det oppstod en feil!', extra_tags='Feil')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'userregistration/editprofile.html', context)

@login_required
def change_password(request):
    user = request.user
    new_password_form = PasswordChangeForm(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    context = {
        'change_password_form': new_password_form,
    }
    return render(request, 'userregistration/changepassword.html', context)




    """
    current_user = request.user
    change_password_form = ChangePasswordForm(request.POST or None, prefix='edit')
    if request.method == 'POST':
        print(0)
        password = change_password_form["password"]
        print(type(password))
        print(password)
        print(current_user.password)
        if password == current_user.password:
            print(1)
            if change_password_form.is_valid():
                print(2)
                password_new = change_password_form['password_new']
                current_user.set_password(password_new)
                messages.add_message(request, messages.SUCCESS, 'Ditt passord er blitt endret', extra_tags='Success')
    context = {
    "change_password_form": change_password_form,
    }
    return render(request, 'userregistration/changepassword.html',context)
    """