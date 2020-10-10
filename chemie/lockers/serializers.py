from rest_framework import serializers
from .models import (
    LockerManager,
    Locker,
    LockerUser,
    OwnershipManager,
    Ownership,
    LockerConfirmationManager,
    LockerToken,
)

# from chemie.customprofile.serializers import UserSerializer


class LockerManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockerManager
        fields = "__all__"


class OwnershipSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Ownership
        fields = "__all__"


class LockerSerializer(serializers.ModelSerializer):
    owner = OwnershipSerializer()

    class Meta:
        model = Locker
        fields = "__all__"


class OwnershipManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnershipManager
        fields = "__all__"


class LockerUserSerializer(serializers.ModelSerializer):
    ownership = LockerSerializer(read_only=True, many=True)

    class Meta:
        model = LockerUser
        fields = "__all__"


class LockerConfirmationManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockerConfirmationManager
        fields = "__all__"


class LockerTokenSerializer(serializers.ModelSerializer):

    ownership = OwnershipSerializer()

    class Meta:
        model = LockerToken
        fields = "__all__"
