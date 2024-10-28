from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile, Medal, User


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
    full_name = serializers.CharField(source="get_full_name", read_only = True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "full_name")
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user = User.objects.create(**user_data)  # Create User instance
        profile = Profile.objects.create(user=user, **validated_data)  # Create Profile instance
        return profile
    
    class Meta:
        model = Profile
        fields = "__all__"

    def update(self, instance, validated_data):
        devices = validated_data.pop('devices', None)
        if devices is not None:
            instance.devices.set(devices)
        return super().update(instance, validated_data)


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = "__all__"


class CatalogSerializer(serializers.ModelSerializer): 
    users = UserSerializer

    class Meta: 
        model = Profile
        fields = "__all__"