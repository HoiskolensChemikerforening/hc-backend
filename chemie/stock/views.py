from django.shortcuts import HttpResponse, render
from .models import Stocktype

# Create your views here.

def index(request):
    return HttpResponse("under constuction")


def stockadmin(request):
    stocktypes = Stocktype.objects.all()
    context = {"stocktypes": stocktypes}

    return render(request, "stock/stockadmin.html", context)