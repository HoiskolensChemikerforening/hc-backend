from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hei <3")


def quiz_term(request, pk):
    return HttpResponse("Verdens beste musikknettside" + str(pk))
