from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stock(models.Model):
    name  = models.CharField(max_length=30)
    desc  = models.TextField()

class History(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stock = models.ManyToManyField(Stock)
    volume = models.IntegerField(null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)




