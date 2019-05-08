from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField


class Specialization(models.Model):
    SPECIALIZATIONS = ((1, 'Bioteknologi'),
                       (2, 'Organisk kjemi'),
                       (3, 'Anvendt teoretisk kjemi'),
                       (4, 'Analytisk kjemi'),
                       (5, 'Kjemisk prosessteknologi'),
                       (6, 'Materialkjemi og energiteknologi'))

    name = models.PositiveSmallIntegerField(choices=SPECIALIZATIONS, unique=True)

    def __str__(self):
        return self.get_name_display()


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Navn")
    description = models.TextField(verbose_name="Beskrivelse")
    logo = ImageField(upload_to="corporate", verbose_name="Logo")
    specializations = models.ManyToManyField(Specialization,
                                             verbose_name="Aktuelle retninger",
                                             blank=True)

    def __str__(self):
        return self.name


class Interview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                verbose_name="Bedrift",
                                blank=True)
    interview_object = models.CharField(max_length=40, verbose_name="Navn på intervjuobjektet")
    text = RichTextField(verbose_name="Intervjuet", config_name="forms")
    picture = ImageField(upload_to="corporate", verbose_name="Bilde")
    specializations = models.ManyToManyField(Specialization,
                                             verbose_name="Aktuelle retninger",
                                             blank=True)
