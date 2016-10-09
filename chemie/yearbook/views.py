from django.shortcuts import render
from customprofile.models import Profile, GRADES, ProfileManager
from django.http import HttpResponseRedirect
from .forms import NameSearchForm

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
        'search_form': NameSearchForm(None),
    }
    return render(request, 'yearbook/get_images.html', context)


def search_user(request):
    if request.method == 'POST':
        form = NameSearchForm(request.POST)
        if form.is_valid():
            name_terms = form.cleaned_data.get('search_field').split(' ')
            profiles = Profile.objects.search_name(name_terms)
            context = {
                'profiles': profiles,
                'search_form': NameSearchForm(None),
            }
            return render(request, 'yearbook/get_images.html', context)
        else:
            return HttpResponseRedirect('/klassekatalog/')
    return HttpResponseRedirect('/klassekatalog/')