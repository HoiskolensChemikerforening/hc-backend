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


COMMENCE_YEAR = 1980
CURRENT_YEAR = datetime.today().year
STIPULATED_TIME = 5
# The last, valid year you can select. 3 years behind the current stipulated year seems reasonable
FINISH_YEAR = CURRENT_YEAR + STIPULATED_TIME + 3
YEARS = [(i, i) for i in range(COMMENCE_YEAR, FINISH_YEAR)]


class Profile(models.Model):
    user = models.OneToOneField(User)

    grade = models.PositiveSmallIntegerField(choices=GRADES, default=GRADES.FIRST)
    allergies = models.CharField(max_length=200)
    start_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR)
    end_year = models.PositiveSmallIntegerField(choices=YEARS, default=CURRENT_YEAR+STIPULATED_TIME)

    phone_number = models.PositiveSmallIntegerField()
    access_card = models.CharField(max_length=10)

    image_primary = ImageField(upload_to='avatars')
    image_secondary = ImageField(upload_to='avatars')
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

