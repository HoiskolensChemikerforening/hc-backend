from django.shortcuts import render, HttpResponse
from django.shortcuts import render
# Create your views here.


def index(request):
    context = {}
    return render(request, "electofeed.html", context)