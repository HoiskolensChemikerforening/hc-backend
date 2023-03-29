from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stocktype(models.Model):
    name  = models.CharField(max_length=30)
    desc  = models.TextField()

    def create_stock(self, amount):
        for i in range(amount):
            stock = Stock()
            stock.stocktype = self
            stock.save()

    def __str__(self):
        return self.name #returnerer navnet på stocken istendenfor dritt


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_markedvalue(self):

        markedvalue = 0

        for stocktype in Stocktype.objects.all():
            stock_amount = len(self.stock_set.filter(stocktype=stocktype))
            value        = stocktype.history_set.order_by("date").first()
            markedvalue += stock_amount*value

        return markedvalue

class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank = True)
    stocktype = models.ForeignKey(Stocktype, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.stocktype} Id:{self.id}"

class History(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    stocktype = models.ForeignKey(Stocktype, on_delete=models.CASCADE)





