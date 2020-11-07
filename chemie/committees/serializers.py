from rest_framework import serializers
from .models import Committee, Position
from chemie.customprofile.serializers import UserSerializer


class CommiteeSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = Committee
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Position
        fields = "__all__"
