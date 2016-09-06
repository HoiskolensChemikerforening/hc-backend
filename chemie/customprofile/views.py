from django.shortcuts import render, get_object_or_404
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import RegisterUserForm, RegisterProfileForm, EditUserForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth import authenticate, login


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


def editprofile(request):
    custom_profile = request.user.profile
    user_profile = custom_profile.user
    user_form = EditUserForm(instance=user_profile)
    profile_form = EditProfileForm(instance=custom_profile)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            context = {
            "title": 'Fullført',
            "message": 'Endringene har blitt registrert',
            "status": 'success',
            }
            return render(request, 'common/feedback.html', context)
    context = {
    "user_form": user_form,
    "profile_form": profile_form
    }
    return render(request, 'userregistration/editprofile.html', context)


def changepassword(request):
    current_user = request.user
    change_password_form = ChangePasswordForm(request.POST or None, prefix='edit')
    if request.method == 'POST':
        if change_password_form.is_valid():
            if change_password_form["password"] == current_user.password:
                user_form.save()
                context = {
                "title": 'Fullført',
                "message": 'Endringene har blitt registrert',
                "status": 'success',
                }
                return render(request, 'common/feedback.html',context)
    context = {
    "change_password_form": change_password_form
    }
    return render(request, 'userregistration/changepassword.html',context)
