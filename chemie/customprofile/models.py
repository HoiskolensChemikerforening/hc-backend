import uuid
from datetime import timedelta
from functools import reduce

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone
from extended_choices import Choices
from sorl.thumbnail import ImageField
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from chemie.shop import statistics
from chemie.web_push.models import Device, Subscription

# Time the activation is valid in hourse
VALID_TIME = 2

# TODO: Decide how to handle weird students aka "PI" / 6th ++ year students
GRADES = Choices(
    ("FIRST", 1, "Første"),
    ("SECOND", 2, "Andre"),
    ("THIRD", 3, "Tredje"),
    ("FOURTH", 4, "Fjerde"),
    ("FIFTH", 5, "Femte"),
    ("DONE", 6, "Ferdig"),
)

RELATIONSHIP_STATUS = Choices(
    ("SINGLE", 1, "Singel"), ("TAKEN", 2, "Opptatt"), ("NSA", 3, "Hemmelig!"), ("HC", 4, "HC incest")
)

MEMBERSHIP_DURATIONS = [
    {"duration_id": 1, "description": "Ettårig"},
    {"duration_id": 2, "description": "Toårig"},
    {"duration_id": 3, "description": "Treårig"},
    {"duration_id": 4, "description": "Fireårig"},
    {"duration_id": 5, "description": "Femårig"},
    {"duration_id": 100, "description": "Livsvarig"},
]

COMMENCE_YEAR = 1980
CURRENT_YEAR = timezone.now().year
STIPULATED_TIME = 5
# The last, valid year you can select. 3 years behind the current stipulated year seems reasonable
FINISH_YEAR = CURRENT_YEAR + STIPULATED_TIME + 3
YEARS = [(i, i) for i in range(COMMENCE_YEAR, FINISH_YEAR)]

SPECIALIZATION = Choices(
    ("NONE", 1, "Ingen"),
    ("ANALYTICAL", 2, "Analytisk kjemi"),
    ("APPLIED", 3, "Anvendt teoretisk kjemi"),
    ("BIOTECH", 4, "Bioteknologi"),
    ("MATERIAL", 5, "Materialkjemi og energiteknologi"),
    ("ORGANICAL", 6, "Organisk kjemi"),
    ("PROCESS", 7, "Kjemisk prosessteknologi"),
)


class ProfileManager(models.Manager):
    def search_name(self, list):
        result = self.filter(
            reduce(
                lambda x, y: x | y,
                [
                    Q(user__first_name__contains=word)
                    | Q(user__last_name__contains=word)
                    for word in list
                ],
            )
        )
        return result

    def get_profile_from_em(self, code):
        try:
            profile = self.filter(access_card=code).first()
        except ObjectDoesNotExist:
            return None
        except None:
            return None
        except:
            raise Http404
        return profile

    @staticmethod
    def rfid_to_em(code):
        # Convert to binary and strip the "0b" prefix
        binary = bin(int(code))[2:]

        # Pad with zeroes on left side
        padded = "0" * (8 - len(binary) % 8) + binary

        # Split into 8-bit groups
        chunked = [
            padded[(i * 8) : (i + 1) * 8] for i in range(0, len(padded) // 8)
        ]

        # Reverse all elements in each group, join groups together
        reversed = "".join([ci[::-1] for ci in chunked])

        # Convert binary back to int
        return int(reversed, 2)


class Medal(models.Model):
    image = ImageField(upload_to="avatars")
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name="Bruker",
    )

    grade = models.PositiveSmallIntegerField(
        choices=GRADES, default=GRADES.FIRST, verbose_name="Klassetrinn"
    )
    start_year = models.PositiveSmallIntegerField(
        choices=YEARS, default=CURRENT_YEAR, verbose_name="Startår"
    )
    end_year = models.PositiveSmallIntegerField(
        choices=YEARS,
        default=CURRENT_YEAR + STIPULATED_TIME,
        verbose_name="Estimert ferdig",
    )
    specialization = models.PositiveSmallIntegerField(
        choices=SPECIALIZATION,
        default=SPECIALIZATION.NONE,
        verbose_name="Spesialisering",
    )

    allergies = models.TextField(
        null=True, blank=True, verbose_name="Matallergi"
    )
    relationship_status = models.PositiveSmallIntegerField(
        choices=RELATIONSHIP_STATUS,
        default=RELATIONSHIP_STATUS.SINGLE,
        verbose_name="Samlivsstatus",
    )

    phone_number = models.BigIntegerField(verbose_name="Mobilnummer")
    access_card = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name="EM nummer (ikke ta med 0 dersom det er første siffer)",
    )

    image_primary = ImageField(upload_to="avatars", null=True, blank=True)
    image_secondary = ImageField(upload_to="avatars", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name="Adresse")

    membership = models.OneToOneField(
        "Membership",
        blank=True,
        null=True,
        related_name="membership",
        on_delete=models.CASCADE,
    )

    approved_terms = models.BooleanField(default=False)

    voted = models.BooleanField(default=False)
    eligible_for_voting = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    devices = models.ManyToManyField(
        Device, blank=True, verbose_name="Push notification-enheter"
    )

    subscriptions = models.ManyToManyField(
        Subscription,
        blank=True,
        verbose_name="Abonnomenter på push-varsler",
        related_name="profile",
    )

    objects = ProfileManager()

    medals = models.ManyToManyField(
        Medal, blank=True, verbose_name="Digidaljer"
    )

    class Meta:
        permissions = (
            ("can_edit_access_card", "Can change access card of profiles"),
            ("refill_balance", "Can refill balance"),
        )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_nice_grade(self):
        return "{}. klasse".format(self.grade)

    def get_nice_relationship_status(self):
        return self.get_relationship_status_display()

    def get_nice_specialization(self):
        return self.get_specialization_display()

    def save(self, *args, **kwargs):
        if self.access_card == "":
            self.access_card = f"{self.pk} - INVALID"
        return super().save(*args, **kwargs)

    """Functions used in shop statics"""

    def get_bought_items(self):
        return statistics.get_bought_items(self.user)

    def get_most_bought_item(self):
        return statistics.get_most_bought_item(self.user)

    def get_second_most_bought_item(self):
        return statistics.get_second_most_bought_item(self.user)

    def get_third_most_bought_item(self):
        return statistics.get_third_most_bought_item(self.user)

    @classmethod
    def get_all_refill_sum(cls):
        return cls.objects.aggregate(Sum("balance"))["balance__sum"]

    @classmethod
    def get_balance_sum_for_first_to_fifth_grades(cls):
        return cls.objects.filter(grade__in=[1, 2, 3, 4, 5]).aggregate(Sum("balance"))["balance__sum"]



class Membership(models.Model):
    start_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    endorser = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_active(self):
        return self.start_date < timezone.now() < self.end_date

    def __str__(self):
        return (
            str(self.start_date.strftime("%d.%m.%Y"))
            + " - "
            + str(self.end_date.strftime("%d.%m.%Y"))
        )


class UserTokenManager(models.Manager):
    def prune_expired(self):
        self.filter(
            created__lt=timezone.now() - timedelta(hours=VALID_TIME)
        ).delete()


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
