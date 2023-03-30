from django import forms
from .models import CGP


class CGPForm(forms.ModelForm):
    class Meta:
        model = CGP
        fields = ()
