from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Medal


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "full_name")


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = "__all__"
