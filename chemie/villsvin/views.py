from django.shortcuts import render
from .models import Villsvin, Sykdom

def index(request):
    a = Villsvin.objects.all()
    b = Sykdom.objects.all()
    context = {"Villsvin": a, "Sykdom": b}

    return render(request, "index.html", context)


