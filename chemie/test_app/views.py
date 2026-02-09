from django.shortcuts import render 
from django.http import HttpResponse


def index(request):

    print("jeg kjører")

    
    context = {}
    return render(request, "jeg_er_fra_test_app.html", context)