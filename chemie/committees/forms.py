from dal import autocomplete
from django import forms

from .models import Committee


class EditDescription(forms.ModelForm):
    class Meta:
        model = Committee
        fields = [
            'description',
            'one_liner',
            'image',
        ]
