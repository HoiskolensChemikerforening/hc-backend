from django import forms
from .models import Refound

class RefoundForm(forms.ModelForm):
    class Meta:
        model = Refound
        fields = ["date", "store", "item", "event", "price", "image"]

