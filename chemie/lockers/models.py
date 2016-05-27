from django.db import models
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

VALID_TIME = 7  # 7 days
LOCKER_COUNT = 2


class Locker(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    owner = models.ForeignKey('Ownership', related_name="definite_owner",
                              null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def is_free(self):
        return self.owner is None

    class Meta:
        ordering = ('number',)

    def reset_idle(self):
        # Fetch all lockers, where an inactive Ownership (through indefinite_locker) is pointing to a locker.
        taken_lockers = self.objects.filter(owner__isnull=False)
        idle_lockers = taken_lockers.filter(indefinite_locker__is_active__exact=False)
        idle_lockers.update(owner="")


class LockerUser(models.Model):
    first_name = models.CharField(max_length=40, default="")
    last_name = models.CharField(max_length=40, default="")
    username = models.EmailField(blank=True, null = True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def reached_limit(self):
        user_locker_count = Ownership.objects.filter(user=self, is_active=True).count()
        return user_locker_count >= LOCKER_COUNT


class Ownership(models.Model):
    locker = models.ForeignKey(Locker, related_name="indefinite_locker")
    user = models.ForeignKey(LockerUser, related_name="User")
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "Locker {} registered to {}".format(self.locker, self.user)

    def prune_expired(self):
        self.objects.filter(is_confirmed=False).delete()

    def create_confirmation(self):
        confirmation_object = LockerConfirmation.objects.create(ownership=self)
        confirmation_object.save()
        return confirmation_object


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

        if self.ownership.user.reached_limit():
            raise ValidationError(_("Du har nådd maksgrensen på ", LOCKER_COUNT, " skap."))

        # Activating ownership
        self.ownership.is_confirmed = True
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

    def prune_expired(self):
        expired_range = datetime.now() - timedelta(days=VALID_TIME)
        self.objects.filter(created__lte=expired_range).delete()
