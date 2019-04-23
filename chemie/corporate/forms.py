from .models import Company, Interview
from django import forms


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description", "logo", "specializations"]


class CreateInterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ["company", "interview_object", "text", "picture"]
