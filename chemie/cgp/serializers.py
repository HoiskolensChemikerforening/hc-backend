from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Vote


class CGPSerializer(serializers.ModelSerializer):
    countryname = SerializerMethodField()
    groupname = SerializerMethodField()
    songname = SerializerMethodField()
    vote = SerializerMethodField()

    def get_countryname(self,vote):
        return vote.group.country.country_name

    def get_groupname(self, vote):
        return vote.group.real_name

    def get_songname(self, vote):
        return vote.group.song_name

    def get_vote(self,vote):
        return vote.vote.replace("]", "").replace("[", "").replace("\"", "").split(",")


    class Meta:
        model = Vote
        fields = ("countryname","groupname","songname","vote")





