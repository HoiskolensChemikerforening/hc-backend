from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CGP

# Create your views here.
@login_required
def index(request):
    cgp = CGP.objects.all()[0]
    countries = cgp.countries.all()
    context = {"countries": countries}

    return render(request, "cgp/index.html", context)