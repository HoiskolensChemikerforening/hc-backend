from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    context = {"committees": 1}

    return render(request, "cgp/index.html", context)