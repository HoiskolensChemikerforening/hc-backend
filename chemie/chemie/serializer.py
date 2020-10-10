from rest_framework import serializers
from django.contrib.auth.models import User
from .models import pictures_for_404, Sponsor

class pictures_for_404Serializer(serializers.ModelSerializer):
    class Meta:
        model = pictures_for_404
        fields = '__all__'

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

