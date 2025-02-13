from django.shortcuts import render
from .models import Villsvin

def index(request):
    a = Villsvin.objects.all()
    context = {}

    return render(request, "index.html", context)