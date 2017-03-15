from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


PRICE_RANGE_CHOICES = (
        (1, 'Under 500 kr'),
        (2, 'Over 500 kr'),
    )


class FundsApplicationModel(models.Model):

    # Application on behalf of ...
    applier = models.CharField(max_length=2000, verbose_name='Søker på vegne av',)

    # Name of person who sent application
    author = models.ForeignKey(User, verbose_name='Innsender')

    # Short description of purpose
    purpose = models.CharField(max_length=2000, verbose_name='Formål')

    # Detailed description of purpose
    description = models.TextField(verbose_name='Beskrivelse',)

    # To which bank account the money would be sent to
    bank_account_id = models.CharField(max_length=11, verbose_name="Kontonummer",
                                       validators=[RegexValidator(
                                           regex='^\d{11}$', message='Kun tall, 11 siffer', code='nomatch')])

    # Name of bank account holder
    bank_account_holder = models.CharField(max_length=2000, verbose_name='Bankkonto innehaver')

    # Price range
    price_range = models.IntegerField(choices=PRICE_RANGE_CHOICES, default=1, verbose_name='Prisklasse')

    # When application is sent
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Receipt
    receipt = models.FileField(upload_to='funds_application', blank=True, null=True, verbose_name="Kvittering")
