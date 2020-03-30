from django import forms
from .models import RentalObject


class RentalObjectForm(forms.ModelForm):
    class Meta:
        model = RentalObject
