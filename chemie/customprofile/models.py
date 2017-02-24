import uuid
from datetime import timedelta
from functools import reduce

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from extended_choices import Choices
from sorl.thumbnail import ImageField

# Time the activation is valid in hours
VALID_TIME = 2

# TODO: Decide how to handle weird students aka "PI" / 6th ++ year students
GRADES = Choices(
    ('FIRST', 1, 'Første'),
    ('SECOND', 2, 'Andre'),
    ('THIRD', 3, 'Tredje'),
    ('FOURTH', 4, 'Fjerde'),
    ('FIFTH', 5, 'Femte'),
    ('DONE', 6, 'Ferdig'),
)

RELATIONSHIP_STATUS = Choices(
    ('SINGLE', 1, 'Singel'),
    ('TAKEN', 2, 'Opptatt'),
    ('NSA', 3, 'Hemmelig!'),
)

COMMENCE_YEAR = 1980
CURRENT_YEAR = timezone.now().year
STIPULATED_TIME = 5
# The last, valid year you can select. 3 years behind the current stipulated year seems reasonable
FINISH_YEAR = CURRENT_YEAR + STIPULATED_TIME + 3
YEARS = [(i, i) for i in range(COMMENCE_YEAR, FINISH_YEAR)]


class ProfileManager(models.Manager):
    def search_name(self, list):
        result = self.filter(reduce(lambda x, y: x | y,
                    [Q(user__first_name__contains=word) | Q(user__last_name__contains=word) for word in list]))
        return result


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    grade = models.PositiveSmallIntegerField(choices=GRADES, default=GRADES.FIRST, verbose_name="Klassetrinn")
    start_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR, verbose_name="Startår")
    end_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR + STIPULATED_TIME,
                                                verbose_name="Estimert ferdig")

    allergies = models.TextField(null=True, blank=True, verbose_name="Matallergi")
    relationship_status = models.PositiveSmallIntegerField(choices=RELATIONSHIP_STATUS,
                                                           default=RELATIONSHIP_STATUS.SINGLE,
                                                           verbose_name="Samlivsstatus")

    phone_number = models.BigIntegerField(verbose_name="Mobilnummer")
    access_card = models.CharField(max_length=20, blank=True, null=True, verbose_name="Studentkortnummer")

    image_primary = ImageField(upload_to='avatars')
    image_secondary = ImageField(upload_to='avatars')
    address = models.CharField(max_length=200, verbose_name="Adresse")

    membership = models.OneToOneField("Membership", null=True, blank=True,related_name="membership")

    objects = ProfileManager()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_nice_grade(self):
        if self.grade == 1:
            return '1. Klasse'
        elif self.grade == 2:
            return '2. Klasse'
        elif self.grade == 2:
            return '3. Klasse'
        elif self.grade == 2:
            return '4. Klasse'
        elif self.grade == 2:
            return '5. Klasse'
        else:
            return 'Ferdig'

    def get_nice_relationship_status(self):
        if self.relationship_status == 1:
            return "Singel"
        elif self.relationship_status == 2:
            return "Opptatt"
        else:
            return "Hemmelig!"


class Membership(models.Model):
    start_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    endorser = models.ForeignKey(User)


    def is_active(self):
        return self.start_date < timezone.now() < self.end_date


class UserTokenManager(models.Manager):
    def prune_expired(self):
        self.filter(created__lt=timezone.now() - timedelta(hours=VALID_TIME)).delete()


class UserToken(models.Model):
    user = models.ForeignKey(User)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = UserTokenManager()

    # Activates the user and deletes the authentication object
    def activate(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    # Set the password and deletes the authentication object
    def set_password(self, password):
        self.user.set_password(password)
        self.user.save()
        self.delete()

    # Checks if the authentication object is expired
    def expired(self):
        return not timezone.now() < timedelta(hours=VALID_TIME) + self.created
