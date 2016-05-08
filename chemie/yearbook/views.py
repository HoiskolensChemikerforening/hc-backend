from django.shortcuts import render
from .models import Profile
import os
import re
# Create your views here.

def index(request):
    context = {

    }
    return render(request, 'yearbook/index.html', context)

def get_images(request, year):
    all_profiles = Profile.objects.filter(year=year)
    context = {
            'profiles': all_profiles,
    }
    return render(request, 'yearbook/get_images.html', context)
