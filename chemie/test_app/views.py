from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):

    print("jeg kjører")

    
    context = {}
    return render(request, "jeg_er_fra_test_app.html", context)


def tamegtiltestapp2(request):
    return redirect("test_app_2:index")