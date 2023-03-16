from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country, CountryPosition
import json


@login_required
def index(request):
    cgp = CGP.objects.all()[0]
    positions = CountryPosition.objects.filter(users=request.user)
    countries = set([p.country for p in positions])
    context = {"countries": countries}

    return render(request, "cgp/index.html", context)

def check_country_access(request, country, manage=False):
    permittedUsersLst = []
    if manage:
        for p in country.countryposition_set.filter(can_manage_country=True):
            permittedUsersLst = permittedUsersLst + list(p.users.all())
    else:
        for p in country.countryposition_set.all():
            permittedUsersLst = permittedUsersLst + list(p.users.all())
    if request.user not in permittedUsersLst:
        return False
    return True

def vote_index(request, slug):
    country = get_object_or_404(Country, slug=slug)
    if not check_country_access(request, country, manage=True):
        return redirect('/cgp')
    cgp = CGP.objects.all()[0]
    countries = cgp.countries.all()
    points = [12,10,8,7,6,5,4,3,2,1]
    if request.method == "POST":
        countryNames = request.POST.getlist("countryNames[]")
        country.vote = json.dumps(countryNames)
        country.save()
        return JsonResponse({"url": reverse("cgp:index")},status=200)

    context = {
        "country": country,
        "countries": ",".join([i.country_name for i in countries]),
        "realnames": ",".join([i.real_name for i in countries]),
        "songtiteles": ",".join([i.song_name for i in countries]),
        "points": ",".join([str(i) for i in points]),
        "url": f"/{slug}/"
               }
    return render(request, "cgp/vote_index.html", context)