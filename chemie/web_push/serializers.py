# api/serializers.py
from rest_framework import serializers
from .models import CoffeeSubmission
from ..chemie.settings.base import PUSH_NOTIFICATIONS_SETTINGS


class CoffeeSubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = CoffeeSubmission
        fields = ["date"]

    def is_authorized(self, token, topic):
        if self.is_valid():
            if token == PUSH_NOTIFICATIONS_SETTINGS["AUTH_TOKEN"]:
                if topic == "coffee":
                    return True
        return False
