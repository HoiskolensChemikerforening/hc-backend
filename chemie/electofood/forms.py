from django import forms
from .models import Answer, VALUES
import material as M

class AnswerForm(forms.Form):
    """class Meta:
        model = Answer
        fields = [
            "answer",
        ]"""
    answer = forms.ChoiceField(choices=VALUES, widget=forms.RadioSelect)