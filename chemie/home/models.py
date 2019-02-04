from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


PRICE_RANGE_CHOICES = ((1, "Under 500 kr"), (2, "Over 500 kr"))


class FundsApplication(models.Model):

    # Application on behalf of ...
    applier = models.CharField(
        max_length=2000, verbose_name="Søker på vegne av"
    )

    # Name of person who sent application
    author = models.ForeignKey(
        User, verbose_name="Innsender", on_delete=models.CASCADE
    )

    # Short description of purpose
    purpose = models.CharField(max_length=2000, verbose_name="Formål")

    # Detailed description of purpose
    description = models.TextField(verbose_name="Beskrivelse")

    # To which bank account the money would be sent to
    bank_account_id = models.BigIntegerField(
        verbose_name="Kontonummer",
        validators=[
            RegexValidator(
                regex="^(\d{10}|\d{11})$",
                message="Kun tall, 11 siffer",
                code="nomatch",
            )
        ],
    )

    # Name of bank account holder
    bank_account_holder = models.CharField(
        max_length=100, verbose_name="Bankkonto innehaver"
    )

    # Price range
    price_range = models.IntegerField(
        choices=PRICE_RANGE_CHOICES, default=1, verbose_name="Prisklasse"
    )

    # When application is sent
    created = models.DateTimeField(auto_now=False, auto_now_add=True)


class OfficeApplication(models.Model):
    # Name of person who sent application
    author = models.ForeignKey(
        User, verbose_name="Innsender", on_delete=models.CASCADE
    )
    # When application is sent
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    # The users student username
    student_username = models.CharField(
        max_length=20, default="NOT_VALID", verbose_name="Studentbrukernavn"
    )

    def __str__(self):
        return f'{self.author.get_full_name()} - {self.student_username}'
