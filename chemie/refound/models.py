from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class RefoundRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])

    def get_total(self):
        total = 0
        for refound in self.refound_set.all():
            total += refound.price
        return total


    def __str__(self):
        return f"{self.created.date()} {self.user.last_name} Total: {self.get_total()}"


class Refound(models.Model):
    refoundrequest = models.ForeignKey(RefoundRequest, on_delete=models.CASCADE)
    date = models.DateField()
    store = models.CharField(max_length=50)
    item = models.CharField(max_length=500)
    event = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to="receipts")

    def __str__(self):
        return f"{self.date} {self.event} Total: {self.price}"



