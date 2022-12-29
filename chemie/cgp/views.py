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
    context = {"country": country}
    return render(request, "cgp/vote_index.html", context)