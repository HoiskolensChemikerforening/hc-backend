from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField


class Specialization(models.Model):
    SPECIALIZATIONS = (
        (1, "Bioteknologi"),
        (2, "Organisk kjemi"),
        (3, "Anvendt teoretisk kjemi"),
        (4, "Analytisk kjemi"),
        (5, "Kjemisk prosessteknologi"),
        (6, "Materialkjemi og energiteknologi"),
    )

    name = models.PositiveSmallIntegerField(
        choices=SPECIALIZATIONS, unique=True
    )

    def __str__(self):
        return self.get_name_display()


class Interview(models.Model):
    interview_object = models.CharField(
        max_length=40, verbose_name="Navn på intervjuobjektet"
    )
    text = RichTextField(verbose_name="Intervjuet", config_name="forms")
    picture = ImageField(upload_to="corporate", verbose_name="Bilde")
    specializations = models.ManyToManyField(
        Specialization, verbose_name="Aktuelle retninger", blank=True
    )

    def __str__(self):
        return self.interview_object


class JobAdvertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name="Stilling")
    description = RichTextField(
        verbose_name="Beskrivelse", config_name="forms"
    )
    is_current = models.BooleanField(verbose_name="Er gjeldende", default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
