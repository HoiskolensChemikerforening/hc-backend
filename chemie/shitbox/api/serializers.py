from rest_framework import serializers
from ..models import Submission
from .fields import Base64ImageField


class SubmissionSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Submission
        fields = ("content", "image", "date")
