from django.shortcuts import render
from .models import Travelletter, Experience, Questions
# Create your views here.

def index(request):
    travelletters = Travelletter.objects.all()
    context = {"travelletter": travelletters}
    return render(request, "index.html", context)


