from .models import Interview
from django import forms


class CreateInterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ["interview_object", "text", "picture"]
