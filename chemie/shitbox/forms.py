from django import forms

from .models import Submission

class Postform(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            "title",
            "content"
        ]