from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Book(models.Model):
    content = models.TextField(max_length=2000, verbose_name="Title")
    cover = ImageField(
        upload_to="shitbox", blank=True, null=True, verbose_name="Cover"
    )
    date = models.DateTimeField(verbose_name="Dato")
    author = models.ForeignKey(
        User, verbose_name="Innsender", on_delete=models.CASCADE
    )
    used = models.BooleanField(
        default=False
    )  # For Sugepumpa to keep track on used submissions

class User(models.Model):
    navn=models.CharField(max=100)
    age=models.PositiveIntegerField()

