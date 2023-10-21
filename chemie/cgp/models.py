from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.utils import timezone
from django.urls import reverse

# Points list: 12 points to country at index 0, ...
POINTS = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]


def reverse_sort_dict_keys(dictionary):
    """
    Sorts the keys of a dictionary by value in reverse order.
    Args:
        dictionary: dict
    Returns:
        sorted keys of the dictionary (key with the highest value first): list
    """
    return [
        i[0]
        for i in sorted(
            dictionary.items(), key=lambda item: item[1], reverse=True
        )
    ]


def add_to_dict(dictionary, key, value):
    """
    Adds a key value pair to a dictionary or increases the value if the key already exists.
    Args:
        dictionary (to be edited): dict
        key (to be inserted)
        value (to be inserted)
    Return:
        dictionary (updated)
    """
    if key in dictionary.keys():
        dictionary[key] += value
    else:
        dictionary[key] = value
    return dictionary


class CGP(models.Model):
    """
    CGP object related to all the data needed for a years Chemie Grand Prix.
    Fields:
        is_open: Boolean (Manages if people can vote. The default is false can be opened through admin page.)
        year: IntegerField(Year of the CGP. Unique to due to the regularity of one CGP per year.)
    Related:
        group_set: queryset (Group objects)
    """

    """
    Todo test 2 publikum countries
    year er egentlig data unique slik at man bare kan lage en cgp per år men akkurat nå er det per dag. Vet ikke om det breaker logikken et setd
    """
    is_open = models.BooleanField(verbose_name="Er åpent", default=False)
    year = models.IntegerField(unique=True, verbose_name="År")

    @classmethod
    def create_new_cgp(cls):
        """
        Classmethod to create new CGP.
        Sets the year field to the current year and is_open to False.
        Args:
            cls: class
        Return:
            cgp: CGP object
        """
        current_year = int(timezone.now().year)
        if CGP.objects.filter(year=current_year):
            return None
        return CGP.objects.create(is_open=False, year=int(timezone.now().year))

    @classmethod
    def get_latest_active(cls):
        """
        Classmethod to get the latest active CGP object.
        Args:
            cls: class
        Return:
            cgp: CGP object (latest open instance) or None (if no instance is open)
        """
        cgps = CGP.objects.filter(is_open=True).order_by("-year")
        if not cgps:
            return None
        return cgps[0]

    @classmethod
    def get_amount_open(cls):
        """
        Classmethod to get amount of open CGP instances.
        Args:
            cls: class
        Return:
            amount: int
        """
        return len(CGP.objects.filter(is_open=True))

    @classmethod
    def get_latest_or_create(cls):
        """
        Classmethod to get the latest CGP object. Creates a new CGP object if there are no CGP objects.
        Args:
            cls: class
        Return:
            cgp: CGP object
        """
        cgps = CGP.objects.order_by("-year")
        if not cgps:
            return cls.create_new_cgp()
        return cgps[0]

    def toggle(self, user):
        """
        Toggles the boolean variable self.is_open (Equivalent to open or closing the possibility to vote).
        Generates the audience vote on close.
        Args:
            self: CGP object
            user: User object (should be the current user)
        Returns:
            None
        """
        if self.is_open:
            self.generate_audience_vote(user)
        self.is_open = not self.is_open
        self.save()
        return

    def generate_audience_vote(self, user):
        """
        Calculates the audience vote by analyzing the related audience votes if there are audience votes.
        Args:
            self: CGP object
            user: User object (should be the current user)
        Returns:
            None
        """
        if len(Group.objects.filter(cgp=self).filter(audience=True)) > 0:
            all_audience_votes = Vote.objects.filter(group__cgp=self).filter(
                group__audience=True
            )
            audience_votes = all_audience_votes.filter(final_vote=False)
            audience_final_votes = all_audience_votes.filter(final_vote=True)
            if len(audience_votes) > 0:
                vote_dict = {}
                show_vote_dict = {}
                failure_vote_dict = {}
                for vote in audience_votes:
                    for count, country in enumerate(
                        vote.vote.replace("]", "")
                        .replace("[", "")
                        .replace('"', "")
                        .split(",")
                    ):
                        if count >= len(POINTS):
                            break
                        vote_dict = add_to_dict(
                            vote_dict, country, POINTS[count]
                        )
                    show_vote_dict = add_to_dict(
                        show_vote_dict, vote.showprize_vote, 1
                    )
                    failure_vote_dict = add_to_dict(
                        failure_vote_dict, vote.failureprize_vote, 1
                    )

                if len(audience_final_votes) > 0:
                    audience_final_vote = audience_final_votes[0]
                else:
                    audience_final_vote = Vote()
                    audience_final_vote.final_vote = True
                    audience_final_vote.group = Group.objects.filter(
                        cgp=self
                    ).get(audience=True)
                audience_final_vote.user = user
                audience_final_vote.vote = ",".join(
                    reverse_sort_dict_keys(vote_dict)
                )
                audience_final_vote.showprize_vote = reverse_sort_dict_keys(
                    show_vote_dict
                )[0]
                audience_final_vote.failureprize_vote = reverse_sort_dict_keys(
                    failure_vote_dict
                )[0]
                audience_final_vote.save()
        return


def __str__(self):
    return f"{self.year}"


class Country(models.Model):
    """
    Country object containing the country name, image and slug. Countries can be used in different
    groups that can be related to different CGPs to prevent uploading the same images each year.
    Fields:
        country_name: CharField (Name of the country is unique)
        image: ImageField (Country flag)
        slug: SlugField (Generated by slugifing country_name in views)
    Related:
        group_set: queryset (Group objects)
    """

    country_name = models.CharField(
        max_length=50, unique=True, verbose_name="Navn"
    )
    image = ImageField(
        upload_to="cgp", null=True, blank=True, verbose_name="Bilde"
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.country_name

    def get_absolute_url(self):
        """
        Gets the url which leads to the voting page for this country.
        Args:
            self: Country objects
        Returns:
            url: str
        """
        return reverse("cgp:vote_index", kwargs={"slug": self.slug})


class Group(models.Model):
    """
    Group object containing the data of a participating group.
    Fields:
        real_name: CharField (name of the group)
        country: ForeignKey (related Country object)
        cgp: ForeignKey (related CGP object)
        song_name: CharField (name of the song)
        audience: BooleanField (is this group the audience? yes/no)
        has_voted: BooleanField (is there a final vote object for this group? yes/no)
        group_leaders: ManyToManyField (User objects with permissions to vote)
        group_members: ManyToManyField (User objects that are a part of this group)
    Related:
        vote_set.all(): queryset (Vote objects (created by the group))
        failurevote.all(): queryset (Vote objects (created by other groups))
        showvote.all(): queryset (Vote objects (created by other groups))
    """

    real_name = models.CharField(max_length=50, verbose_name="Gruppenavn")
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, verbose_name="Land"
    )
    cgp = models.ForeignKey(CGP, on_delete=models.CASCADE)
    song_name = models.CharField(
        max_length=100, blank=True, verbose_name="Sangtittel"
    )
    audience = models.BooleanField(verbose_name="Publikum", default=False)
    has_voted = models.BooleanField(verbose_name="Har stemt", default=False)
    group_leaders = models.ManyToManyField(
        User, related_name="group_leaders", blank=True, verbose_name="Ledere"
    )
    group_members = models.ManyToManyField(
        User,
        related_name="group_members",
        blank=True,
        verbose_name="Medlemmer",
    )

    def __str__(self):
        return f"{self.real_name}"

    def delete(self, using=None, keep_parents=False):
        """
        Overrides the delete method to delete all related votes.
        """
        for group in self.cgp.group_set.all():
            for vote in group.vote_set.all():
                if self.country.country_name in vote.vote.replace(
                    "]", ""
                ).replace("[", "").replace('"', "").split(","):
                    vote.delete()
        return super().delete(using=None, keep_parents=False)


class Vote(models.Model):
    """
    Vote object containing the data of a single vote.
    Fields:
        final_vote: BooleanField (differentiates between every single persons vote and the mean vote)
        group: ForeignKey (Group object connected to the creation of the vote)
        user: ForeignKey (User object connected to the creation of the vote)
        vote: TextField (country names in a string in order to preserve the ranking)
        failureprize_vote: ForeignKey (Group object which received the failureprize vote)
        showprize_vote: ForeignKey (Group object which received the showprize vote)
    """

    final_vote = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.TextField(blank=True)
    failureprize_vote = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="failurevote"
    )
    showprize_vote = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="showvote"
    )

    def get_sorted_groups_list(self):
        """
        Translates the vote string into an ordered list with Group objects
        and fetches the showprize and failureprize vote.
        Args:
            self: Vote object
        Returns:
            group_list: list (Ordered list containing Group objects)
            self.failureprize_vote: Group (Group object which received the failureprize vote)
            self.showprize_vote: Group  (Group object which received the showprize vote)
        """
        vote_list = (
            self.vote.replace("]", "")
            .replace("[", "")
            .replace('"', "")
            .split(",")
        )
        vote_dict = {vote_list[i]: i for i in range(len(vote_list))}
        group_list = sorted(
            list(
                self.group.cgp.group_set.exclude(id=self.group.id).exclude(
                    audience=True
                )
            ),
            key=lambda group: vote_dict[group.country.country_name],
        )
        return group_list, self.failureprize_vote, self.showprize_vote
