from django import forms
from django.contrib.auth.models import User
from .models import Picture
import material as M

class Pictureform(forms.ModelForm):
    layout = M.Layout(M.Row('picture'),
                      M.Row('description'))

    class Meta:
        model = Picture
        fields = [
            "picture",
            "description"
        ]
