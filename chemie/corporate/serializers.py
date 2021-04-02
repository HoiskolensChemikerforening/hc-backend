from rest_framework import serializers
from .models import Interview, Job, Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_name_display")

    class Meta:
        fields = ("id", "name")
        model = Specialization


class InterviewSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "interview_object",
            "text",
            "picture",
            "specializations",
        )
        model = Interview


class JobSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "job_object",
            "description",
            "specializations",
        )
        model = Job
