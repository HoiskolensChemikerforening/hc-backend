from django.shortcuts import render
from customprofile.models import Profile, GRADES
from .forms import NameSearchForm
from django.db.models import Q
from django.contrib.auth.models import User


def index(request, year=1):
    year = int(year)
    if year not in GRADES:
        if year > GRADES.FIFTH.value:
            year = GRADES.FIFTH.value
        else:
            year = 1
    form = NameSearchForm(request.POST or None)
    profiles = Profile.objects.none()
    if request.method == 'POST':
        if form.is_valid():
            search_field = form.cleaned_data.get('search_field')
            users = find_user_by_name(search_field)
            profiles = Profile.objects.filter(user__in=users)
    else:
        profiles = Profile.objects.filter(grade=year)
    context = {
        'profiles': profiles,
        'grades': GRADES,
        'search_form': form,
    }
    return render(request, 'yearbook/get_images.html', context)


def find_user_by_name(query_name):
    qs = User.objects.all()
    for term in query_name.split():
        qs = qs.filter( Q(first_name__icontains=term) | Q(last_name__icontains=term))
    return qs
