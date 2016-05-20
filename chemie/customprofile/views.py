from django.shortcuts import render
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from .forms import RegisterUserForm, RegisterProfileForm


def register_user(request):
    user_core_form = RegisterUserForm(request.POST or None)
    user_profile_form = RegisterProfileForm(request.POST or None)

    if user_core_form.is_valid() and user_profile_form.is_valid():
        pass

    context = {
        "user_core_form": user_core_form,
        "user_profile_form": user_profile_form,
    }
    return render(request, 'userregistration/register.html', context)
