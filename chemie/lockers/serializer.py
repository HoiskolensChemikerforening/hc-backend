from rest_framework import serializers
from .models import LockerManager, Locker, LockerUser, Ownership, LockerToken

from chemie.customprofile.serializers import UserSerializer


class LockerManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockerManager
        fields = "__all__"


class LockerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockerUser
        fields = "__all__"


class OwnershipSerializer(serializers.ModelSerializer):
    user = LockerUserSerializer()

    class Meta:
        model = Ownership
        fields = "__all__"


class LockerSerializer(serializers.ModelSerializer):
    owner = OwnershipSerializer()

    class Meta:
        model = Locker
        fields = "__all__"


class LockerTokenSerializer(serializers.ModelSerializer):
    ownership = OwnershipSerializer(read_only=True, many=True)

    class Meta:
        model = LockerToken
        fields = "__all__"
