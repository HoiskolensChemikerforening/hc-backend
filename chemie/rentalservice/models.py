from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField


class RentalObject(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(verbose_name="Beskrivelse", config_name="news")
    image = ImageField(upload_to="rentalservice", verbose_name="Bilde")

    def __str__(self):
        return self.name