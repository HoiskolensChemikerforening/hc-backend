from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Vote


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
        return vote.vote.replace("]", "").replace("[", "").replace("\"", "").split(",")

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
            "showprize_vote"
        )





