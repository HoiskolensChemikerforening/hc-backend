from django.db import models
from sorl.thumbnail import ImageField
from multiselectfield import MultiSelectField
from django.urls import reverse


SPECIALIZATIONS = ((1, 'Bioteknologi'),
                   (2, 'Organisk kjemi'),
                   (3, 'Anvendt teoretisk kjemi'),
                   (4, 'Analytisk kjemi'),
                   (5, 'Kjemisk prosessteknologi'),
                   (6, 'Materialkjemi og energiteknologi'))


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Navn")
    description = models.TextField(verbose_name="Beskrivelse")
    logo = ImageField(upload_to="corporate", verbose_name="Logo")
    specializations = MultiSelectField(choices=SPECIALIZATIONS, verbose_name="Aktuelle retninger")

    def __str__(self):
        return self.name


class Interview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Bedrift")
    name = models.CharField(max_length=40, verbose_name="Navn")
    interview = models.TextField(verbose_name="Intervjuet")
    picture = ImageField(upload_to="corporate", verbose_name="Bilde")

    def get_absolute_url(self):
        return reverse(
            "corporate:interview", kwargs={"interview_id": self.id}
        )
