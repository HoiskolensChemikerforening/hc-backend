from django.db import models
from django.contrib.auth.models import User


class MerchCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]  # Ordering elements by name in dropdown


class Merch(models.Model):
    name = models.CharField(max_length=40, verbose_name="Navn")
    price = models.FloatField(verbose_name="Pris")
    image = models.ImageField(upload_to="merch", verbose_name="Bilde")
    info = models.TextField(
        max_length=500, blank=True, verbose_name="Beskrivelse"
    )
    category = models.ForeignKey(
        MerchCategory,
        verbose_name="Kategori",
        related_name="Category",
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        return self.name
