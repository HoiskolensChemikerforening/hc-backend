from django.db import models
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Locker(models.Model):
    number = models.PositiveSmallIntegerField()
    # ownership = models.ForeignKey(Ownership)

    def __str__(self):
        return str(self.number)


class LockerUser(models.Model):
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    username = models.CharField(max_length=10, blank=True, unique=True)
    internal_user = models.ForeignKey(User, null=True, blank=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')

    def __str__(self):
        if (self.internal_user):
            return(internal_user.username)
        else:
            return(self.first_name + " " + self.last_name)

    def clean(self):
        if self.internal_user:
            if (self.first_name or self.last_name or self.username):
                raise ValidationError(_("Fyll ut enten din interne bruker " +
                                        "eller navn og brukernavn."))
        elif not (self.first_name and self.last_name and self.username):
            raise ValidationError(_("Du må fylle ut alle tre feltene."))

    class Meta:
        unique_together = ("first_name", "last_name")

class Ownership(models.Model):
    locker = models.ForeignKey(Locker)
    user = models.ForeignKey(LockerUser, related_name="User")
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    activation_code = models.UUIDField(default=uuid)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Locker " + self.locker + " registered to " + self.user
