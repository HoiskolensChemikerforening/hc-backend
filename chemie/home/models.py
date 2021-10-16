from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from sorl.thumbnail import ImageField


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
        return f"{self.author.get_full_name()} - {self.student_username}"


class RefundApplication(models.Model):
    """
    Contains several RefundItems.
    The application can be approved or denied by board members.
    """
    STATUS = (
        (1, "Waiting"),
        (2, "Approved"),
        (3, "Denied"),
    )

    date = models.DateField(verbose_name="Dato")
    name = models.CharField(max_length=50, verbose_name="Navn")
    receipt = ImageField(upload_to="refund", verbose_name="Kvittering")
    account_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex='^\d{11}$', message='Kontonummeret må bestå av 11 siffer')], 
        verbose_name="Kontonummer"
        )
    status = models.PositiveSmallIntegerField(
        choices=STATUS, default=1
    )

    def __str__(self):
        return str(self.date) + " - " + str(self.name)


class RefundItem(models.Model):
    # Contains information about the bought items for which refund is applied for

    date = models.DateField(verbose_name="Utleggsdato")
    store = models.CharField(max_length=100, verbose_name="Kjøpssted")
    item = models.CharField(max_length=100, verbose_name="Vare")
    event = models.CharField(max_length=100, verbose_name="Arrangement")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Pris")
    application = models.ForeignKey(RefundApplication, related_name="items", on_delete=models.CASCADE, verbose_name="Søknad")

    def __str__(self):
        return str(self.date) + " - " + str(self.item)
