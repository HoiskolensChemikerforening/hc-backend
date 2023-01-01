from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.urls import reverse
from django.template.defaultfilters import slugify

class Country(models.Model):
    """
    A CGP country containing user objects elegible to vote for this country
    """
    country_name = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=50)
    image = ImageField(upload_to="cgp", null=True, blank=True)
    users = models.ManyToManyField(User, blank=True, verbose_name="medlem")
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)
    slug = models.SlugField(null=True, blank=True,editable=False)

    def __str__(self):
        return self.country_name

    def get_absolute_url(self):
        return reverse("cgp:vote_index", kwargs={"slug": self.slug})

    def save(self):
        if not self.slug:
            self.slug = slugify(self.country_name)

        super(Country, self).save()




class CGP(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    countries = models.ManyToManyField(Country, blank=True, verbose_name="country")

    @classmethod
    def create_new_election(cls):
        CGP.objects.create(is_open=True)

