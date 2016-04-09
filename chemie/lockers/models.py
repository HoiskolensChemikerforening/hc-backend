from django.db import models
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



class Locker(models.Model):
    number = models.PositiveSmallIntegerField()


class LockerUser(models.Model):
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    username = models.CharField(max_length=10, blank=True)
    internal_user = models.ForeignKey(User, null=True, blank=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')
    def clean(self):
        if (self.internal_user and (self.first_name or self.last_name or self.username)):
            raise ValidationError(_("Fyll ut enten din interne bruker eller navn og brukernavn."))
        if not (self.first_name and self.last_name and self.username):
            raise ValidationError(_("Du må fylle ut alle tre feltene."))


class Ownership(models.Model):
    locker = models.ForeignKey(Locker)
    user = models.ForeignKey(LockerUser)
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    activation_code = models.UUIDField(default=uuid)
    active = models.BooleanField(default=False)
