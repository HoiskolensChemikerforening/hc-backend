from django.shortcuts import render
from .models import Villsvin, Sykdom
from .forms import VillsvinForm

def index(request):
    a = Villsvin.objects.all()
    b = Sykdom.objects.all()
    context = {"Villsvin": a, "Sykdom": b}

    return render(request, "index.html", context)


def createVillsvin(request):
    form = VillsvinForm()

    context = {"form":form}
    

    return render(request, "villsvinform.html", context)




