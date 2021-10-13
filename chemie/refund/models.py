from django.db import models
from sorl.thumbnail import ImageField


class Refund(models.Model):
    date = models.DateField(verbose_name="Utleggsdato")
    store = models.CharField(verbose_name="Kjøpssted")
    item = models.CharField(verbose_name="Vare")
    event = models.CharField(verbose_name="Event")
    price = models.FloatField(verbose_name="Pris")

    def __str__(self):
        return str(self.date) + str(self.item)


class RefundForm(models.Model):
    STATUS = (
        (1, "Waiting"),
        (2, "Approved"),
        (3, "Denied"),
    )

    refunds = models.ForeignKey(
        Refund, related_name="refusjon", on_delete=models.CASCADE
    )
    date = models.DateField(verbose_name="Dato")
    name = models.CharField(max_length=50, verbose_name="Navn")
    receipt = ImageField(upload_to="refund", verbose_name="Kvittering")
    account = models.IntegerField(verbose_name="Kontonummer")
    status = models.PositiveSmallIntegerField(
        choices=STATUS, unique=True
    )

    def __str__(self):
        return str(self.date)+str(self.name)