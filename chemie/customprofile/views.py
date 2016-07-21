from django.shortcuts import render
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import RegisterUserForm, RegisterProfileForm
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


