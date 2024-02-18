from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile, Medal


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims. Add profile id
        try:
            profile_id = Profile.objects.get(user=user).id
        except ObjectDoesNotExist:
            profile_id = None

        token["profile_id"] = profile_id

        return token


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "full_name")

class UserSerializerWithId(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "full_name")



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = "__all__"
