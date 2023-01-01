from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country
import json

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
    if request.method == "POST":
        countryNames = request.POST.getlist("countryNames[]")
        country.vote = json.dumps(countryNames)
        country.save()
        return JsonResponse({"url": reverse("cgp:index")},status=200)

    context = {
        "country": country,
        "countries": ",".join([i.country_name for i in countries]),
        "points": ",".join([str(i) for i in points]),
        "url": f"/{slug}/"
               }
    return render(request, "cgp/vote_index.html", context)