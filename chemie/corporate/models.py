from django.db import models
from sorl.thumbnail import ImageField


SPECIALIZATIONS = ((1, 'Bioteknologi'),
                   (2, 'Organisk kjemi'),
                   (3, 'Anvendt teoretisk kjemi'),
                   (4, 'Analytisk kjemi'),
                   (5, 'Kjemisk prosessteknologi'),
                   (6, 'Materialkjemi og energiteknologi'))


class Interview(models.Model):
    corporate = models.ForeignKey(Company, on_delete=models.CASCADE)
    person = models.CharField(max_length=40)
    text = models.TextField(
        verbose_name="Selve Intervjuet"
    )
    picture = models.ImageField()


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="corporate", verbose_name="Logo")
    #specializations = models.(choices=SPECIALIZATIONS)

    def __str__(self):
        return self.name
