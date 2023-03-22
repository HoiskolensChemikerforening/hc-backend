from django.shortcuts import HttpResponse, render, get_object_or_404
from .models import Stocktype
from .forms import StocktypeForm
# Create your views here.

def index(request):
    return HttpResponse("under constuction")


def stockadmin(request):
    stocktypes = Stocktype.objects.all()

    if request.method == 'POST':
        form = StocktypeForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            amount = form.cleaned_data['amount']
            stocktype = Stocktype()
            stocktype.name = name
            stocktype.desc = desc
            stocktype.save()
            stocktype.create_stock(amount)

            form = StocktypeForm()

    else:
        form = StocktypeForm()

    context = {"stocktypes": stocktypes,
               "form" : form
    }
    return render(request, "stock/stockadmin.html", context)

def individual(request,id):
    stocktypeobject = get_object_or_404(Stocktype, id=id)
    stocks = stocktypeobject.stock_set.all()
    context = {"stocktypeobject": stocktypeobject,
               "stocks":stocks}

    return render(request, "stock/individual.html", context)

