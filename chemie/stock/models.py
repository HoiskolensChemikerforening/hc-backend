from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stock(models.Model):
    name  = models.CharField(max_length=30)
    desc  = models.TextField()

class History(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=None, decimal_places=2)
    stock = models.OneToOneField(Stock)

class Porofolio(models.Model):
    user = models.OneToOneField(User)
    stock = models.OneToOneField(Stock)
    volume = models.IntegerField(null=True)
    balance = models.DecimalField(max_digits=None, decimal_places=2)




