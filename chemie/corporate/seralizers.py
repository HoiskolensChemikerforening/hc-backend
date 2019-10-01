from rest_framework import serializers
from .models import Company, Interview, Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')

    class Meta:
        fields = (
            'id',
            'name',
        )
        model = Specialization


class CompanySerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'logo',
            'specializations'
        )
        model = Company


class InterviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    specializations = SpecializationSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'company',
            'interview_object',
            'text',
            'picture',
            'specializations'
        )
        model = Interview
