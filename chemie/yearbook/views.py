from django.shortcuts import render
from .models import Profile
import os
import re
# Create your views here.

def index(request):
    all_profiles = Profile.objects.all()
    for profile in all_profiles:
        print(profile.image)
    context = {
            'profiles': all_profiles,
    }
    return render(request, 'yearbook/index.html', context)
