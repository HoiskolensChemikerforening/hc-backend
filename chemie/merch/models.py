from django.db import models
from django.contrib.auth.models import User

class Merch(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="merch", verbose_name="Bilde")

    def __str__(self):
        return self.name



