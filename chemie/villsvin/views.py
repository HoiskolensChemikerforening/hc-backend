from django.shortcuts import render
from .models import Villsvin, Sykdom
from .forms import VillsvinForm
from django.contrib import messages

def index(request):
    a = Villsvin.objects.all()
    b = Sykdom.objects.all()
    context = {"Villsvin": a, "Sykdom": b}

    return render(request, "index.html", context)


def createVillsvin(request):
    form = VillsvinForm()
    print(0)
    if request.method == "POST":
        form = VillsvinForm(data = request.POST)
        print(1)
        print(form)
        print("#"*40)
        print(request.POST)
        print("#"*40)
        print(form.errors)
        if form.is_valid():
            print(2)
            form_instance = form.save(commit=False)
            form_instance.save()
            form.save_m2m()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Villsvin er lagret",
            )



    context = {"form":form}
    

    return render(request, "villsvinform.html", context)




