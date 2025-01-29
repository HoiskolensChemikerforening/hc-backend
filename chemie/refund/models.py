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


class RefundRequest(models.Model):
    """
    The refund request object contains information about the user requesting a
    refund. It is connected to one or more Refund objects (receipts) which contain further information.
    """

    # Variable containing the user requesting a refund
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
        for refund in self.refund_set.all():
            total += refund.price
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
        Returns the amount of receipts (Refund objects) related to this object.
        """
        return len(self.refund_set.all())

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
    def get_refund_request_annual(cls, year):
        """
        Get a queryset containing all RefundRequest objects related to a receipt (Refund) from a specified
        year. RefundRequest objects can be related to multiple Refund objects (receipts). Those receipts can be from
        different years. The oldest receipt determines the year used for filtering the RefundRequest object.
        """
        return (
            cls.objects.filter(refund__date__year=year)
            .exclude(refund__date__year__lt=year)
            .distinct()
        )


class Refund(models.Model):
    """
    The refund object contains the data from a specific receipt. It is related to a RefundRequest.
    """

    # Variable containing the related RefundRequest object
    refundrequest = models.ForeignKey(RefundRequest, on_delete=models.CASCADE)
    # Variable containing the date of the receipt
    date = models.DateField(verbose_name="Utleggsdato")
    # Variable containing the name of the store
    store = models.CharField(max_length=50, verbose_name="Kjøpssted")
    # Variable containing the items bought.
    item = models.CharField(max_length=500, verbose_name="Varer")
    # Variable containing the event or reason why the items have been bought
    event = models.CharField(max_length=50, verbose_name="Hensikt/Arragement")
    # Variable containing the price of the items bought
    price = models.IntegerField(
        verbose_name="Pris", validators=[MinValueValidator(0)]
    )
    # Variable containing an image of the receipt
    image = models.ImageField(upload_to="receipts", verbose_name="Kvittering")

    def __str__(self):
        return f"{self.date} {self.event} Total: {self.price}"
