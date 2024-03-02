from django import forms
from .models import Word, Category



class WordInput(forms.ModelForm):

    class Meta:
        model = Word
        fields = ["word", "explanations", "date", "picture", "secret"]

