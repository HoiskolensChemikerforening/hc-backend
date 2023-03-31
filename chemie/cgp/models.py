import datetime

from django.db import models
from django.contrib.auth.models import User#, Group
from chemie.customprofile.models import Profile
from sorl.thumbnail import ImageField
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from extended_choices import Choices



POINTS = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]

def reverse_sort_dict_keys(dictionary):
    return [i[0] for i in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)]

def add_to_dict(dictionary,key, value):
    if key in dictionary.keys():
        dictionary[key] += value
    else:
        dictionary[key] = value
    return dictionary


class CGP(models.Model):
    """
    Todo test 2 publikum countries
    year er egentlig data unique slik at man bare kan lage en cgp per år men akkurat nå er det per dag. Vet ikke om det breaker logikken et setd
    """
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    year = models.IntegerField(unique=True, verbose_name="År")

    @classmethod
    def create_new_cgp(cls):
        return CGP.objects.create(is_open=False, year=int(timezone.now().year))

    @classmethod
    def get_latest_active(cls):
        """
        returns the latest open CGP object.
        returns None if no CGP is open.
        """
        cgps = CGP.objects.filter(is_open=True).order_by("-year")
        if not cgps:
            return None
        return cgps[0]


    @classmethod
    def get_amount_open(cls):
        return len(CGP.objects.filter(is_open=True))


    @classmethod
    def get_latest_or_create(cls):
        cgps = CGP.objects.order_by("-year")
        if not cgps:
            return cls.create_new_cgp()
        return cgps[0]

    def toggle(self, user):
        if self.is_open and len(Group.objects.filter(cgp=self).filter(audience=True)) > 0:
            all_audience_votes = Vote.objects\
                .filter(group__cgp=self)\
                .filter(group__audience=True)
            audience_votes = all_audience_votes.filter(final_vote=False)
            audience_final_votes = all_audience_votes.filter(final_vote=True)
            if len(audience_votes)> 0:
                vote_dict = {}
                show_vote_dict = {}
                failure_vote_dict = {}
                for vote in audience_votes:
                    for count, country in enumerate(vote.vote.replace("]", "").replace("[", "").replace("\"", "").split(",")):
                        if count >= len(POINTS):
                            break
                        vote_dict = add_to_dict(vote_dict, country, POINTS[count])
                    show_vote_dict = add_to_dict(show_vote_dict, vote.showprize_vote, 1)
                    failure_vote_dict = add_to_dict(failure_vote_dict, vote.failureprize_vote, 1)

                if len(audience_final_votes) > 0:
                    audience_final_vote = audience_final_votes[0]
                else:
                    audience_final_vote = Vote()
                    audience_final_vote.final_vote = True
                    audience_final_vote.group = Group.objects.filter(cgp=self).get(audience=True)
                audience_final_vote.user = user
                audience_final_vote.vote = ",".join(reverse_sort_dict_keys(vote_dict))
                audience_final_vote.showprize_vote =reverse_sort_dict_keys(show_vote_dict)[0]
                audience_final_vote.failureprize_vote =reverse_sort_dict_keys(failure_vote_dict)[0]
                audience_final_vote.save()
        self.is_open = not self.is_open
        self.save()
        return


def __str__(self):
    return f"{self.year}"

class Country(models.Model):
    """
    A CGP country containing user objects elegible to vote for this country
    """
    country_name = models.CharField(max_length=50, unique=True)
    image = ImageField(upload_to="cgp", null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.country_name

    def get_absolute_url(self):
        return reverse("cgp:vote_index", kwargs={"slug": self.slug})



class Group(models.Model):
    """
    username unique publikum vote for different years :(
    """
    #group_username = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    cgp = models.ForeignKey(CGP, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100, blank=True)
    audience = models.BooleanField(verbose_name="Publikum", default=False)
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)
    group_leaders = models.ManyToManyField(User, related_name="group_leaders", blank=True)
    group_members = models.ManyToManyField(User, related_name="group_members", blank=True)

    def __str__(self):
        return f"{self.real_name}"



class Vote(models.Model):
    final_vote = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.TextField(blank=True)
    failureprize_vote = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="failurevote")
    showprize_vote = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="showvote")








