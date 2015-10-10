from django.db import models
from django.contrib.auth.models import User
from mezzanine.pages.models import Page


class Accounts(models.Model):
    user = models.ForeignKey(User, verbose_name="Kontoinnehaver")
	balance = models.PositiveIntegerField(verbose_name="Kontobalanse")

class Transactions(models.Model):
        account = models.ForeignKey("Accounts")
        item_list = models.ManyToManyField('Items')


class Items(Page):
    scan_code = models.PositiveIntegerField(unique=True,
                                            verbose_name="Barkode",
                                            )
    ACTIVATED = 1
    DEACTIVATED = 0
    STATUS_CHOICES = (
        (ACTIVATED,'Aktiv'),
        (DEACTIVATED, 'Ikke aktiv')
    )
    status_condition = models.IntegerField(blank=False,
                              max_length=1,
                              choices=STATUS_CHOICES,default=ACTIVATED,
                              verbose_name="Status",
                              )

    published_date = models.DateTimeField(verbose_name="Publisert",
                                          auto_now_add=True,
                                          )

    picture = models.ImageField()
    author = models.ForeignKey(User, verbose_name="Opprettet av")
    price = models.PositiveSmallIntegerField(blank=False,
                                             verbose_name="Pris")

    class Meta:
        verbose_name = ("Vare")
        verbose_name_plural = ("Varer")