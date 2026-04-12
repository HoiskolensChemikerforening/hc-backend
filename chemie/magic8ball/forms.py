from django import forms
import material as M
from .models import MagicAnswer

class EightBallForm(forms.Form):
    sporsmal = forms.CharField(
        label='Hva lurer du på?', 
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Vil jeg bestå eksamen?'})
    )

    

