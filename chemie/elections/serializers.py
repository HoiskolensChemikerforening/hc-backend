from rest_framework import serializers
from .models import Candidate


class CGPSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.first_name")

    class Meta:
        model = Candidate
        fields = ("votes", "pre_votes", "user")
