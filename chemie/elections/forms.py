from django import forms

from .models import Vote

class Postform (forms.ModelForm):
    class Meta:
        model = Vote
        fields = [
        "candidate",
        "ticket"
        ]
