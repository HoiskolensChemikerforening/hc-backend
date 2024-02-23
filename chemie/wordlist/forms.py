from django import forms
from .models import Word, Category



class WordInput(forms.ModelForm):

    class Meta:
        model = Word
        fields = "__all__"

