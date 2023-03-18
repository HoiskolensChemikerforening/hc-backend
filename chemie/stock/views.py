from django.shortcuts import HttpResponse, render, get_object_or_404
from .models import Stocktype

# Create your views here.

def index(request):
    return HttpResponse("under constuction")


def stockadmin(request):
    stocktypes = Stocktype.objects.all()
    context = {"stocktypes": stocktypes}

    return render(request, "stock/stockadmin.html", context)

def individual(request,id):
    stocktypeobject = get_object_or_404(Stocktype, id=id)
    stocks = stocktypeobject.stock_set.all()
    context = {"stocktypeobject": stocktypeobject,
               "stocks":stocks}

    return render(request, "stock/individual.html", context)

