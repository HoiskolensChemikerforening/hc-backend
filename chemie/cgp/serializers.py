from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Vote


class CGPSerializer(serializers.ModelSerializer):
    countryname = SerializerMethodField()
    groupname = SerializerMethodField()
    songname = SerializerMethodField()
    vote = SerializerMethodField()
    failureprize_vote = SerializerMethodField()
    showprize_vote = SerializerMethodField()

    def get_countryname(self,vote):
        return vote.group.country.country_name

    def get_groupname(self, vote):
        return vote.group.real_name

    def get_songname(self, vote):
        return vote.group.song_name

    def get_vote(self,vote):
        return vote.vote.replace("]", "").replace("[", "").replace("\"", "").split(",")
    def get_failureprize_vote(self,vote):
        return vote.failureprize_vote.country.country_name
    def get_showprize_vote(self,vote):
        return vote.showprize_vote.country.country_name
    class Meta:
        model = Vote
        fields = ("countryname","groupname","songname","vote", "failureprize_vote", "showprize_vote")





