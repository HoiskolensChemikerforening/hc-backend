from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Jeg elsker Pia og Marthe <3</h1>")
