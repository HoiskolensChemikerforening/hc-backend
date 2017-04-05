from django.db import models
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from .validators import validate_NTNU

VALID_TIME = 7  # 7 days
LOCKER_COUNT = 2


class LockerManager(models.Manager):
    def reset_idle(self):
        # Fetch all lockers, where an inactive Ownership (through indefinite_locker) is pointing to a locker.
        taken_lockers = self.filter(owner__isnull=False)
        idle_lockers = taken_lockers.filter(indefinite_locker__is_active__exact=False)
        idle_lockers_count = idle_lockers.update(owner=None)
        return idle_lockers_count


class Locker(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    owner = models.ForeignKey('Ownership', related_name="definite_owner",
                              null=True, blank=True)

    objects = LockerManager()

    def __str__(self):
        return str(self.number)

    def is_free(self):
        return self.owner is None

    def get_absolute_url(self):
        return reverse("bokskap:registrer", kwargs={"number": self.number})

    def clear(self):
        self.owner.is_active = False
        self.owner.save()
        self.owner = None

    class Meta:
        ordering = ('number',)


class LockerUser(models.Model):
    first_name = models.CharField(max_length=40, verbose_name="Fornavn")
    last_name = models.CharField(max_length=40, verbose_name="Etternavn")
    email = models.EmailField(validators=[validate_NTNU], verbose_name="NTNU-epost")
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def reached_limit(self):
        user_locker_count = Ownership.objects.filter(user=self, is_active=True).count()
        return user_locker_count >= LOCKER_COUNT

    def fetch_lockers(self):
        return Locker.objects.filter(owner__user=self)


class OwnershipManager(models.Manager):
    def prune_expired(self):
        self.filter(is_confirmed=False).delete()

    def fetch_all_states(self):
        taken_lockers = self.objects.filter(definite_owner__owner__isnull=False)
        taken_lockers = taken_lockers.prefetch_related("user")
        return taken_lockers


class Ownership(models.Model):
    locker = models.ForeignKey(Locker, related_name="indefinite_locker")
    user = models.ForeignKey(LockerUser, related_name="User")
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    objects = OwnershipManager()

    def __str__(self):
        return "Locker {} registered to {}".format(self.locker.number, self.user)

    def create_confirmation(self):
        confirmation_object = LockerToken.objects.create(ownership=self)
        confirmation_object.save()
        return confirmation_object

    def reached_limit(self):
        return self.user.reached_limit()


class LockerConfirmationManager(models.Manager):
    def prune_expired(self):
        expired_range = timezone.now() - timedelta(days=VALID_TIME)
        self.filter(created__lte=expired_range).delete()


class LockerToken(models.Model):
    ownership = models.ForeignKey(Ownership)
    key = models.UUIDField(default=uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LockerConfirmationManager()

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
        return not timezone.now() < timedelta(days=VALID_TIME) + self.created

    def __str__(self):
        return str(self.ownership.locker)

    def reactivate(self):
        self.ownership.is_active = True
        self.ownership.save()
        self.delete()

    def get_absolute_url(self):
        return reverse('bokskap:activate', kwargs={'code': self.key.hex})
