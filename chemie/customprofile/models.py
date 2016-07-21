from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from extended_choices import Choices
from datetime import datetime

# TODO: Decide how to handle weird students aka "PI" / 6th ++ year students
GRADES = Choices(
    ('FIRST',  1, 'Første'),
    ('SECOND', 2, 'Andre'),
    ('THIRD',  3, 'Tredje'),
    ('FOURTH', 4, 'Fjerde'),
    ('FIFTH',  5, 'Femte'),
    ('DONE',   6, 'Ferdig'),
)

RELATIONSHIP_STATUS = Choices(
    ('SINGLE',  1, 'Singel'),
    ('TAKEN', 2, 'Opptatt'),
    ('COMPLICATED',  3, 'Det er komplisert...'),
    ('GUESS', 4, 'Gjett ;)'),
    ('NSA',  5, 'Hemmelig!'),
)
COMMENCE_YEAR = 1980
CURRENT_YEAR = datetime.today().year
STIPULATED_TIME = 5
# The last, valid year you can select. 3 years behind the current stipulated year seems reasonable
FINISH_YEAR = CURRENT_YEAR + STIPULATED_TIME + 3
YEARS = [(i, i) for i in range(COMMENCE_YEAR, FINISH_YEAR)]


class Profile(models.Model):
    user = models.OneToOneField(User)

    grade = models.PositiveSmallIntegerField(choices=GRADES, default=GRADES.FIRST, verbose_name="Klassetrinn")
    start_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR, verbose_name="Startår")
    end_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR+STIPULATED_TIME,
                                                verbose_name="Estimert ferdig")

    allergies = models.TextField(null=True, blank=True, verbose_name="Matallergi")
    relationship_status = models.PositiveSmallIntegerField(choices=RELATIONSHIP_STATUS,
                                                           default=RELATIONSHIP_STATUS.SINGLE,
                                                           verbose_name="Samlivsstatus")

    phone_number = models.PositiveSmallIntegerField(verbose_name="Mobilnummer")
    access_card = models.CharField(max_length=10, unique=True, verbose_name="Studentkortnummer")

    image_primary = ImageField(upload_to='avatars')
    image_secondary = ImageField(upload_to='avatars')
    address = models.CharField(max_length=200, verbose_name="Adresse")

    membership = models.OneToOneField("Membership", null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Membership(models.Model):
    start_date = models.DateField(auto_now=False, auto_now_add=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    endorser = models.ForeignKey(User)

    def is_active(self):
        return self.start_date < datetime.now() < self.end_date
