from django.db import models
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

VALID_TIME = 14  # 2 Weeks
LOCKER_COUNT = 2


class Locker(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    owner = models.ForeignKey("Ownership", related_name="Owner",
                              null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def is_free(self):
        return self.owner is None

    class Meta:
        ordering = ('number',)


class LockerUser(models.Model):
    first_name = models.CharField(max_length=40, default="")
    last_name = models.CharField(max_length=40, default="")
    username = models.EmailField(blank=True, null = True)
    internal_user = models.ForeignKey(User, null=True, blank=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')

    def __str__(self):
        if self.internal_user:
            return str(self.internal_user.profile)
        else:
            return self.first_name + " " + self.last_name

    def clean(self):
        if self.internal_user:
            if self.first_name or self.last_name or self.username:
                raise ValidationError(_("Fyll ut enten din interne bruker " +
                                        "eller navn og brukernavn."))
        elif not (self.first_name and self.last_name and self.username):
            raise ValidationError(_("Du må fylle ut alle tre feltene."))

    def reached_limit(self):
        user_locker_count = Ownership.objects.filter(user=self, is_active=True).count()
        return user_locker_count >= 2


class Ownership(models.Model):
    locker = models.ForeignKey(Locker)
    user = models.ForeignKey(LockerUser, related_name="User")
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "Locker {} registered to {}".format(self.locker, self.user)


class LockerConfirmation(models.Model):
    ownership = models.ForeignKey(Ownership)
    key = models.UUIDField(default=uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def activate(self):
        # Confirm that the locker is free
        if self.ownership.locker.owner is not None:
            if self.ownership.locker.owner != self.ownership:
                raise ValidationError(_("Skapet er tatt"))
        else:
            ValidationError(_("Du eier allerede skapet."))

        # Activating ownership
        self.ownership.is_active = True
        # Binding the locker to the ownership
        self.ownership.locker.owner = self.ownership
        self.ownership.locker.save()
        self.ownership.save()
        self.delete()

    def expired(self):
        return not datetime.now() < timedelta(days=VALID_TIME) + self.created

    def __str__(self):
        return str(self.ownership.locker)
