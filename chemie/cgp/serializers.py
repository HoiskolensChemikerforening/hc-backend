from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Vote, Country, Group, CGP


class CGPSerializer(serializers.ModelSerializer):
    """
    Generates the CGP API.
    Fields:
        countryname: str (name of the voting country)
        groupname: str (name of the voting group)
        songname: str (songtitle of the voting group)
        vote: list (ordered list containing countrynames (highest to lowest amount of points))
        failureprize_vote: str (name of the failureprize country)
        showprize_vote: str (name of the showprize country)
    """

    countryname = SerializerMethodField()
    groupname = SerializerMethodField()
    songname = SerializerMethodField()
    vote = SerializerMethodField()
    failureprize_vote = SerializerMethodField()
    showprize_vote = SerializerMethodField()

    def get_countryname(self, vote):
        """
        Gets the name of the voting country.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            countryname: str
        """
        return vote.group.country.country_name

    def get_groupname(self, vote):
        """
        Gets the name of the voting group.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            groupname: str
        """
        return vote.group.real_name

    def get_songname(self, vote):
        """
        Gets the songtitle of the voting group.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            songname: str
        """
        return vote.group.song_name

    def get_vote(self, vote):
        """
        Gets an ordered list containing countrynames of the vote.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            vote: list
        """
        return (
            vote.vote.replace("]", "")
            .replace("[", "")
            .replace('"', "")
            .split(",")
        )

    def get_failureprize_vote(self, vote):
        """
        Gets the name of the failureprize country.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            failureprize_vote: str
        """
        return vote.failureprize_vote.country.country_name

    def get_showprize_vote(self, vote):
        """
        Gets the name of the showprize country.
        Args:
            self: CGPSerializer object
            vote: Vote object
        Returns:
            showprize_vote: str
        """
        return vote.showprize_vote.country.country_name

    class Meta:
        model = Vote
        fields = (
            "countryname",
            "groupname",
            "songname",
            "vote",
            "failureprize_vote",
            "showprize_vote",
        )


class GroupSerializer(serializers.ModelSerializer):
    """
    Generates the CGP Group API. Displays all the Groups related to the current CGP.
    Fields:
        countryname: str (name of the country)
        real_name: str (name of the group)
        song_name: str (songtitle of the group)
        audience: boolean (is the group the audience)
        countryimage: str (url to the corresponding country image)
        year: int (CGP year)
    """

    countryname = SerializerMethodField()
    countryimage = SerializerMethodField()
    year = SerializerMethodField()

    def get_countryname(self, group):
        """
        Gets the name of the group country.
        Args:
            self: GroupSerializer object
            group: Group object
        Returns:
            countryname: str
        """
        return group.country.country_name

    def get_countryimage(self, group):
        """
        Gets the url of the group country image.
        Args:
            self: GroupSerializer object
            group: Group object
        Returns:
            countryimageurl: str
        """
        request = self.context.get("request")
        return request.build_absolute_uri(group.country.image.url)

    def get_year(self, group):
        """
        Gets the year of the CGP.
        Args:
            self: GroupSerializer object
            group: Group object
        Returns:
            year: int
        """
        return group.cgp.year

    class Meta:
        model = Group
        fields = (
            "countryname",
            "real_name",
            "song_name",
            "audience",
            "countryimage",
            "year",
        )
