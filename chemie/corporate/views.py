from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Interview

# Create your views here.


def index(request):
    return HttpResponse("Du er sykt heft10")


def interview(request):
    interviews = Interview.objects.order_by("id")
    context = {"interviews": interviews}

    return render(request, "corporate/interview.html", context)

