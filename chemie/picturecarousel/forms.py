from django import forms
from django.contrib.auth.models import User
from .models import Submission
import material as M


class Pictureform(forms.ModelForm):
    layout = M.Layout(M.Row('file'))

    class Meta:
        model = Submission
        fields = [
            "image",
        ]
