from django.shortcuts import HttpResponse, render, get_object_or_404
from .models import Stocktype, Stock
from .forms import StocktypeForm, StockOwnerName, Portfolio
from django.contrib.auth.models import User

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
               "form": form
    }
    return render(request, "stock/stockadmin.html", context)


def individual(request,id):
    stocktypeobject = get_object_or_404(Stocktype, id=id)
    stocks = stocktypeobject.stock_set.all()
    context = {"stocktypeobject": stocktypeobject,
               "stocks":stocks}

    return render(request, "stock/individual.html", context)


def individualadmin(request, id, individual_id):
    stock = get_object_or_404(Stock, id=individual_id)

    if request.method == 'POST':
        form = StockOwnerName(request.POST)

        if form.is_valid():
            portfolio = form.cleaned_data['portfolio']
            stock.portfolio = portfolio
            stock.save()

            form = StockOwnerName()

    else:
        form = StockOwnerName()


    form = StockOwnerName()
    context = {"form": form}

    return render(request,"stock/individualadmin.html", context)


