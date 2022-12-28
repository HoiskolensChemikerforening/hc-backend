from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

class Country(models.Model):
    """
    A CGP country containing user objects elegible to vote for this country
    """
    country_name = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=50)
    image = ImageField(upload_to="cgp", null=True, blank=True)
    users = models.ManyToManyField(User, blank=True, verbose_name="medlem")
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)




class CGP(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    countries = models.ManyToManyField(Country, blank=True, verbose_name="country")

    @classmethod
    def create_new_election(cls):
        CGP.objects.create(is_open=True)

