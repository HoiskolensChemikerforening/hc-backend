from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Cult
from .forms import CultForms


def index(request):

    context = {}
    return render(request, "krokodille.html", context)


def index_2(request): # http://127.0.0.1:8000/test_app_2/krokodille_2/

    all_cults = Cult.objects.all()

    if request.method == "POST":
        form = CultForms(request.POST)
        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt spørsmål opprettet!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect("test_app_2:index_2")


    else:
        form = CultForms()

    context = {"html_form":form, "html_cults":all_cults}


    return render(request, "krokodille2.html", context)


def dih(request):
    context = {}
    #return HttpResponseRedirect(reverse("test_app:jeg_er_fra_test_app"))
    # return render(request, "test_app:jeg_er_fra_Test_app.html", context)
    print("dih kjører")
    return redirect("test_app:index")

