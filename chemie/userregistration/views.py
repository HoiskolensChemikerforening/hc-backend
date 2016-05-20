from django.shortcuts import render
from customprofile.models import Profile, GRADES
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from .forms import RegisterUser, RegistrationForm

def register_user(request):
    form = 0
    if request.method =='POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            if form.password == form.password_confirm:
                Profile.user.password = form.password
            else:
                raise Http404
        Profile.user.first_name = form.first_name
        Profile.user.last_name = form.last_name
        Profile.user.username = form.username
        Profile.user.email = form.email
        Profile.grade = form.grade
        Profile.allergies = form.allergies
        Profile.start_year = form.start_year
        Profile.end_year = form.end_year
        Profile.phone_number = form.phone_number
        Profile.access_card = form.access_card
        Profile.image_primary = form.image_primary
        Profile.save()
    context = {
        "form": form,
    }
    return render(request, 'userregistration/post_form.html', context)
