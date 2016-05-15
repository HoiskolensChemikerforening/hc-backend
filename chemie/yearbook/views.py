from django.shortcuts import render
from customprofile.models import Profile, GRADES


def index(request, year=1):
    year = int(year)
    if year not in GRADES:
        if year > GRADES.FIFTH.value:
            year = GRADES.FIFTH.value
        else:
            year = 1

    profiles = Profile.objects.filter(grade=year)
    context = {
        'profiles': profiles,
        'grades': GRADES,
    }
    return render(request, 'yearbook/get_images.html', context)
