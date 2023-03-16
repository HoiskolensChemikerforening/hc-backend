from django.db import models
from django.contrib.auth.models import User, Group
from sorl.thumbnail import ImageField
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

class Country(models.Model):
    """
    A CGP country containing user objects elegible to vote for this country
    """
    country_name = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=50)
    song_name = models.CharField(max_length=100, blank=True)
    image = ImageField(upload_to="cgp", null=True, blank=True)
    #group_leader_user = models.ForeignKey(CountryPosition, blank=True, verbose_name="leader", on_delete=models.CASCADE())
    #users = models.ForeignKey(CountryPosition, blank=True, verbose_name="leader", on_delete=models.CASCADE())
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)
    vote = models.TextField(blank=True)
    slug = models.SlugField(null=True, blank=True,editable=False)

    def __str__(self):
        return self.country_name

    def get_absolute_url(self):
        return reverse("cgp:vote_index", kwargs={"slug": self.slug})

    def get_group_members(self):
        return self.users

    def save(self):
        if not self.slug:
            self.slug = slugify(self.country_name)

        super(Country, self).save()


class CountryPosition(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    max_members = models.PositiveSmallIntegerField(
        default=1, verbose_name="Antall medlemmer"
    )
    can_manage_country = models.BooleanField(default=False)
    users = models.ManyToManyField(User, blank=True, verbose_name="medlem")
    """
    def remove_from_group(self, users):
        for user in users:
            self.permission_group.user_set.remove(user)

    def add_to_group(self, users):
        for user in users:
            self.permission_group.user_set.add(user)

    # Signal for adding and removing users from a permission group as they are
    # added/removed to a Position https://stackoverflow.com/a/4571362
    @staticmethod
    def consistent_permissions(
            sender, instance, action, reverse, model, pk_set, **kwargs
    ):

        if action == "pre_add":
            if len(pk_set) + instance.users.count() > instance.max_members:
                raise ValidationError(
                    "This only holds {} members.".format(instance.max_members)
                )

        if action == "post_add":
            instance.add_to_group(instance.users.all())
        elif action == "pre_remove":
            instance.remove_from_group(instance.users.all())"""

    def __str__(self):
        return f"Position for {str(self.country.country_name)}"


class CGP(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    countries = models.ManyToManyField(Country, blank=True, verbose_name="country")

    @classmethod
    def create_new_election(cls):
        CGP.objects.create(is_open=True)

