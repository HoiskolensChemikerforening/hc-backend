from django.shortcuts import render
from .models import Travelletter, Experience, Questions
# Create your views here.

def index(request):
    travelletters = Travelletter.objects.all()
    context = {"travelletter": travelletters}
    return render(request, "index.html", context)


def detailViews(request):
    return render(request, "detail.html")

def createViews(request):
    return render(request, "create.html")




