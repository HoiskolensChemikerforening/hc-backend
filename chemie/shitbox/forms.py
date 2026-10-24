from django import forms
from .models import Submission


class PostForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["content", "image"]
