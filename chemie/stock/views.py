from django.shortcuts import HttpResponse, render, get_object_or_404
from .models import Stocktype, Stock, Portfolio
from .forms import StocktypeForm, StockOwnerName
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from chemie.customprofile.models import Profile



@login_required
def index(request):

    stocktypes   = Stocktype.objects.all()
    #portofolioList = Stocktype.objects.filter()  på høyre side i bildet
    user_portofolio = Portfolio.objects.get(user=request.user)
    markedValue     = user_portofolio.get_markedvalue()
    coins       = request.user.profile.balance

    context = {"stocktypes": stocktypes,
               #"portofolioList": portofolioList,
               "markedValue": markedValue,
               "coins": coins
    }

    return render(request, "stock/stock.html", context)

def stock_index(request):

    #name = Stocktype.name
    #desc
    #volume
    #value

    context = {
    }

    return render(request, "stock/individualstock.html", context)


@login_required
@permission_required("stock.add_stock")
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
               "form": form}

    return render(request, "stock/stockadmin.html", context)

@login_required
@permission_required("stock.add_stock")
def individual(request,id):
    stocktypeobject = get_object_or_404(Stocktype, id=id)
    stocks = stocktypeobject.stock_set.all()
    context = {"stocktypeobject": stocktypeobject,
               "stocks":stocks}

    return render(request, "stock/individual.html", context)

@login_required
@permission_required("stock.add_stock")
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


