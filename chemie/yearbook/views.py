from django.shortcuts import render
from .models import Profile, ProfileImage
import os
# Create your views here.

def index(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_profiles = Profile.objects.all()
    for profile in all_profiles:
        print(profile.image.avatar_thumbnail.url)
    context = {
            'root': BASE_DIR,
            'profiles': all_profiles,
    }
    return render(request, 'yearbook/index.html', context)
