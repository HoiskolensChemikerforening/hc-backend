from rest_framework import serializers
from .models import QuizTerm, QuizScore

# from chemie.customprofile.serializers import UserSerializer

class QuizTermSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizTerm
        fields = "__all__"

class QuizScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = QuizScore
        fields ="__all__"