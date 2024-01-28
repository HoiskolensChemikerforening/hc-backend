from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MinValueValidator
from extended_choices import Choices

STATUS = Choices(
    ("REJECTED", 1, "Avslått"),
    ("PENDING", 2, "Under behandling"),
    ("APPROVED", 3, "Tilbakebetalt"),
)


class RefoundRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)],
        verbose_name="Kontonummer",
    )
    status = models.SmallIntegerField(
        choices=STATUS, default=STATUS.PENDING, verbose_name="Tilbakebetalt"
    )

    def get_total(self):
        total = 0
        for refound in self.refound_set.all():
            total += refound.price
        return total

    def __str__(self):
        return f"{self.created.date()} {self.user.last_name} Total: {self.get_total()}"

    def get_status(self):
        return STATUS[self.status - 1][1]

    def get_amount_receipts(self):
        return len(self.refound_set.all())

    def print_account_number(self):
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
        return cls.objects.filter(refound__date__year=year).exclude(
            refound__date__year__lt=year
        )


class Refound(models.Model):
    refoundrequest = models.ForeignKey(
        RefoundRequest, on_delete=models.CASCADE
    )
    date = models.DateField(verbose_name="Utleggsdato")
    store = models.CharField(max_length=50, verbose_name="Kjøpssted")
    item = models.CharField(max_length=500, verbose_name="Varer")
    event = models.CharField(max_length=50, verbose_name="Hensikt/Arragement")
    price = models.IntegerField(verbose_name="Pris", validators=[MinValueValidator(0)],)
    image = models.ImageField(upload_to="receipts", verbose_name="Kvittering")

    def __str__(self):
        return f"{self.date} {self.event} Total: {self.price}"
