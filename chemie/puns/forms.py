from django import forms
from .models import Puns

class PunsForm(forms.ModelForm):
    class Meta:
        model = Puns
        fields = ['tekstskrive', 'tekstlese']
        widgets = {
            'tekst': forms.Textarea(attrs={'rows': 2}),
        }