from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CGP, Country

# Create your views here.
@login_required
def index(request):
    cgp = CGP.objects.all()[0]
    countries = cgp.countries.all()
    context = {"countries": countries}

    return render(request, "cgp/index.html", context)

@login_required
def vote_index(request, slug):
    country = get_object_or_404(Country, slug=slug)
    cgp = CGP.objects.all()[0]
    countries = cgp.countries.all()
    points = [12,10,8,7,6,5,4,3,2,1]
    pointsCountries = []
    for i in range(max(len(countries),len(points))):
        if i < len(points):
            p = points[i]
        else:
            p = 0
            points.append(0)
        if i < len(countries):
            c = countries[i]
        else:
            c = None
        pointsCountries.append((p,c))


    context = {
        "country": country,
        "pointsCountries": pointsCountries,
        "countries": ",".join([i.country_name for i in countries]),
        "points": ",".join([str(i) for i in points])
               }
    return render(request, "cgp/vote_index.html", context)