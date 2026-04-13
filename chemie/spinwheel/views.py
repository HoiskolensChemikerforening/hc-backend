from django.shortcuts import render
from .forms import SpinWheelForm
import random 

def spin_wheel_view(request):
    form = SpinWheelForm()
    resultat = None
    alternativer = []

    if request.method == 'POST':
        form = SpinWheelForm(request.POST)
        if form.is_valid():
            tekst = form.cleaned_data["alternativer"]
            alternativer = tekst.splitlines()
            alternativer = [alternativ.strip() for alternativ in alternativer if alternativ.strip()]

            if alternativer:
                resultat = random.choice(alternativer)
    
    return render(request, "spinwheel.html", {
        "form": form,
        "resultat": resultat,
        "alternativer": alternativer,
    })
