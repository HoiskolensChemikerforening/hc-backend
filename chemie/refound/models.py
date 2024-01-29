from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from extended_choices import Choices

# Track the status of a request
STATUS = Choices(
    ("REJECTED", 1, "Avslått"),
    ("PENDING", 2, "Under behandling"),
    ("APPROVED", 3, "Tilbakebetalt"),
)


class RefoundRequest(models.Model):
    """
    The refound request object contains information about the user requesting a
    refund. It is connected to one or more Refund objects (receipts) which contain further information.
    """

    # Variable containing the user requesting a refound
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Variable containing the date of the request.
    created = models.DateTimeField(auto_now_add=True)
    # Variable containing the bank account number
    account_number = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)],
        verbose_name="Kontonummer",
    )
    # Variable to keep track of the request's status.
    status = models.SmallIntegerField(
        choices=STATUS, default=STATUS.PENDING, verbose_name="Tilbakebetalt"
    )

    def get_total(self):
        """
        Calculates the total sum the user is requesting.
        """
        total = 0
        for refound in self.refound_set.all():
            total += refound.price
        return total

    def __str__(self):
        return f"{self.created.date()} {self.user.last_name} Total: {self.get_total()}"

    def get_status(self):
        """
        Returns the status of the request as a string.
        """
        return STATUS[self.status - 1][1]

    def get_amount_receipts(self):
        """
        Returns the amount of receipts (Refound objects) related to this object.
        """
        return len(self.refound_set.all())

    def print_account_number(self):
        """
        Returns the bank account number seperated by .
        """
        if len(self.account_number) == 11:
            return (
                self.account_number[:4]
                + "."
                + self.account_number[4:6]
                + "."
                + self.account_number[6:]
            )
        return self.account_number

    @classmethod
    def get_refound_request_annual(cls, year):
        """
        Get a queryset containing all RefoundRequest objects related to a receipt (Refound) from a specified
        year. RefoundRequest objects can be related to multiple Refound objects (receipts). Those receipts can be from
        different years. The oldest receipt determines the year used for filtering the RefoundRequest object.
        """
        return cls.objects.filter(refound__date__year=year).exclude(
            refound__date__year__lt=year
        )


class Refound(models.Model):
    """
    The refound object contains the data from a specific receipt. It is related to a RefoundRequest.
    """

    # Variable containing the related RefoundRequest object
    refoundrequest = models.ForeignKey(
        RefoundRequest, on_delete=models.CASCADE
    )
    # Variable containing the date of the receipt
    date = models.DateField(verbose_name="Utleggsdato")
    # Variable containing the name of the store
    store = models.CharField(max_length=50, verbose_name="Kjøpssted")
    # Variable containing the items bought.
    item = models.CharField(max_length=500, verbose_name="Varer")
    # Variable containing the event or reason why the items have been bought
    event = models.CharField(max_length=50, verbose_name="Hensikt/Arragement")
    # Variable containing the price of the items bought
    price = models.IntegerField(verbose_name="Pris", validators=[MinValueValidator(0)],)
    # Variable containing an image of the receipt
    image = models.ImageField(upload_to="receipts", verbose_name="Kvittering")

    def __str__(self):
        return f"{self.date} {self.event} Total: {self.price}"
