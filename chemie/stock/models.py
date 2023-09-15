from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your models here.

class Stocktype(models.Model):
    name  = models.CharField(max_length=30)
    desc  = models.TextField()

    def create_stock(self, amount):
        for i in range(amount):
            stock = Stock()
            stock.stocktype = self
            stock.save()

    def get_amount(self):
        #returns amout of stocks
        return

    def sell(self, user, amount):
        #sjekk if user has amount stock
        #if yes remove from protfolio and update balance
        return

    def save(self, *args, **kwargs):
        """
        Kjører når et stocktype object lagres i databasen
        """
        super(Stocktype, self).save(*args, **kwargs)
        # add code to generate History objects for self
        # TODO


    def __str__(self):
        return self.name #returnerer navnet på stocken istendenfor dritt


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_markedvalue(self):

        markedvalue = 0

        for stocktype in Stocktype.objects.all():
            stock_amount = len(self.stock_set.filter(stocktype=stocktype))       #stocktype.getstockamount
            value        = stocktype.history_set.order_by("-date").first().value #endrer rekkefølgen i Queryset med "-"
            markedvalue += stock_amount*value

        return markedvalue

    def get_number_of_stocks(self, id):
        stocktype = get_object_or_404(Stocktype, id = id)
        stock_amount = len(self.stock_set.filter(stocktype=stocktype))
        return stock_amount

    def assign_stock_to_portofolio(self, id):
        stocktype = get_object_or_404(Stocktype, id=id)
        new_stock = stocktype.create_stock(1)
        new_stock.portfolio = self
        return new_stock

    def __str__(self):
        return f"{self.user.username}"

class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank = True)
    stocktype = models.ForeignKey(Stocktype, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.stocktype} Id:{self.id}"

class History(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    stocktype = models.ForeignKey(Stocktype, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stocktype} {self.date.strftime('%d.%m.%Y')}"






