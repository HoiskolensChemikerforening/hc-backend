from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import SerializerMethodField

from chemie.customprofile.serializers import UserSerializer
from django.utils import timezone
from .models import OfficeApplication

class OfficeAccessSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    alreadyApplied = SerializerMethodField()
    class Meta:
        model = OfficeApplication
        fields = "__all__"
    def get_alreadyApplied(self, test):
        author = self.request.user  # hente student username fra form
        already_applied = OfficeApplication.objects.filter(
        author=author, created__gte=timezone.now() - timezone.timedelta(days=30),).exists()
        return already_applied