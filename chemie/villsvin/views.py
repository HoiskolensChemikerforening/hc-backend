from django.shortcuts import render
from .models import Villsvin, Sykdom
from .forms import VillsvinForm
from django

def index(request):
    a = Villsvin.objects.all()
    b = Sykdom.objects.all()
    context = {"Villsvin": a, "Sykdom": b}

    return render(request, "index.html", context)

def createVillsvin(request):
    form = VillsvinForm()

    if request.method == "POST":
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.save()
            form.save_m2m()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Villsvin er lagret",
            )

    
    context = {"form":form}
    return render(request, "Villsvin.html")

