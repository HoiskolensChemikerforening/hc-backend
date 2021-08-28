from django.db import models
from django.contrib.auth.models import User


class MerchCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Merch(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="merch", verbose_name="Bilde")
    info = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(MerchCategory, related_name="Category", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

