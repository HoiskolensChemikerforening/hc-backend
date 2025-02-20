from django.db import models


class Villsvin(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"

class Korv(models.Model):
    weight = models.DecimalField(decimal_places=2, max_digits=8)
    length = models.DecimalField(decimal_places=2, max_digits=8)
    name = models.CharField(max_length=30)
    boar = models.ForeignKey(Villsvin, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.weight}"


class Sykdom(models.Model):
    disease_name = models.CharField(max_length=100)
    mortality = 