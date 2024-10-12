from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Social,
    Bedpres,
    SocialEventRegistration,
    BedpresRegistration,
)

from chemie.customprofile.serializers import UserSerializer
from chemie.committees.serializers import CommitteeSerializer


class AttendeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")
    grade = serializers.IntegerField(source="profile.grade")
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "full_name", "grade")


class SocialSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    committee = CommitteeSerializer()
    confirmed_attendees = AttendeeSerializer(read_only=True, many=True, source="get_confirmed_users")
    waiting_attendees = AttendeeSerializer(read_only=True, many=True, source="get_waiting_users")
    class Meta:
        model = Social
        fields = "__all__"


class SocialEventRegistrationSerializer(serializers.ModelSerializer):
    event = SocialSerializer()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SocialEventRegistration
        fields = "__all__"


class BedpresSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    confirmed_attendees = AttendeeSerializer(read_only=True, many=True, source="get_confirmed_users")
    waiting_attendees = AttendeeSerializer(read_only=True, many=True, source="get_waiting_users")

    class Meta:
        model = Bedpres
        fields = "__all__"


class BedpresRegistrationSerializer(serializers.ModelSerializer):
    event = BedpresSerializer()
    user = UserSerializer()

    class Meta:
        model = BedpresRegistration
        fields = "__all__"
