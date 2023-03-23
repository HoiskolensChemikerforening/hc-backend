import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from sorl.thumbnail import ImageField
from django.urls import reverse
from django.template.defaultfilters import slugify


class CGP(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    year = models.DateField(auto_now_add=True, unique=True)
    @classmethod
    def create_new_election(cls):
        CGP.objects.create(is_open=True)

    @classmethod
    def get_latest_active(cls):
        return CGP.objects.filter(is_open=True).order_by("-year")[0]

    def __str__(self):
        return f"{self.year}"

class Country(models.Model):
    """
    A CGP country containing user objects elegible to vote for this country
    """
    country_name = models.CharField(max_length=50, unique=True)
    image = ImageField(upload_to="cgp", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True,editable=False)

    def __str__(self):
        return self.country_name

    def get_absolute_url(self):
        return reverse("cgp:vote_index", kwargs={"slug": self.slug})


    def save(self):
        if not self.slug:
            self.slug = slugify(self.country_name)

        super(Country, self).save()


class Group(models.Model):
    group_username = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    cgp = models.ForeignKey(CGP, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100, blank=True)
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)

    def __str__(self):
        return f"{self.real_name}"


class CgpPosition(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    max_members = models.PositiveSmallIntegerField(
        default=1, verbose_name="Antall medlemmer"
    )
    can_manage_country = models.BooleanField(default=False)
    users = models.ManyToManyField(User, blank=True, verbose_name="medlem")

    def __str__(self):
        return f"Position for {str(self.group.country.country_name)}"


class Vote(models.Model):
    final_vote = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.TextField(blank=True)





