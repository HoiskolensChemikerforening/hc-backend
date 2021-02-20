from django.db import models

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from chemie.committees.models import Committee
from django.core.validators import MaxValueValidator, MinValueValidator


class Landlord(models.Model):  # Utleier aka promokom/ac
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

    def __str__(self):
        return self.committee.title


class RentalObject(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(verbose_name="Beskrivelse", config_name="news")
    image = ImageField(upload_to="rentalservice", verbose_name="Bilde")
    owner = models.ForeignKey(
        Landlord, null=True, blank=True, on_delete=models.CASCADE
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )  # Trenger min og maks verdi
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )  # Trenger min og maks verdi

    def __str__(self):
        return self.name
