from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Travelletter, Experience, Questions, Images
from chemie.customprofile.serializers import UserSerializer


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class TravelletterSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Travelletter
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    question = QuestionsSerializer()
    travelletter = TravelletterSerializer()

    class Meta:
        model = Experience
        fields = "__all__"


