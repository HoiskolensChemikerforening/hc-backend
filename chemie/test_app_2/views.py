from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):

    print("jeg kjører")

    
    context = {}
    return render(request, "krokodille.html", context)


def index_2(request):
    context = {}

    return render(request, "krokodille2.html", context)

def dih(request):
    context = {}
    #return HttpResponseRedirect(reverse("test_app:jeg_er_fra_test_app"))
    return render(request, "test_app:jeg_er_fra_Test_app.html", context)