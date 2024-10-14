from rest_framework import serializers
from .models import Committee, Position, User
from chemie.customprofile.serializers import UserSerializer


class CommitteeSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = Committee
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True)

    class Meta:
        model = Position
        fields = "__all__"
