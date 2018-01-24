from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Submission
        fields = ('content', 'image', 'date', 'author')
