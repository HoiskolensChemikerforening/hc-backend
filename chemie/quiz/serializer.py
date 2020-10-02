from rest_framework import serializers
from .models import QuizTerm, QuizScore
from django.contrib.auth.models import User

# from chemie.customprofile.serializers import UserSerializer


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "full_name")


class QuizTermSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizTerm
        fields = "__all__"

class QuizScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = QuizScore
        fields ="__all__"