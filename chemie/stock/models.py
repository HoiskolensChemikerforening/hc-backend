from django.db import models

# Create your models here.

class Stock(models.Model):
    name  = models.CharField(max_length=30)
    desc  = models.TextField()

class History(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=None, decimal_places=2)
    stock = models.OneToOneField(Stock)


