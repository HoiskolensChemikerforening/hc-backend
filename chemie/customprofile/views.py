from django.shortcuts import render
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import RegisterUserForm, RegisterProfileForm, UserLoginForm
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

def user_login(request):
    login_form = UserLoginForm(request.POST or None)
    context = {
    "login_form": login_form
    }
    if login_form.is_valid():
        username = login_form.username
        password = login_form.password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context = {
                "message": 'Du er nå inlogget!'
                }
                return render(request, 'common/feedback.html', context)
            else:
                context = {
                "message": "Brukeren eksisterer ikke"
                }
                return render(request, 'common/feedback.html', context)
        else:
            context={
            "message": "Beklager, enten passord eller bruknavnet er feil."
            }
            return render(request, 'common/feedback.html', context)

    return render(request, 'userregistration/login.html', context)
