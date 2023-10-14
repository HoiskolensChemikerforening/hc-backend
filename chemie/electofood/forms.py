from django import forms
from .models import Answer, VALUES, ElectionQuestionForm, ElectionQuestion
import material as M

class AnswerForm(forms.Form):
    """class Meta:
        model = Answer
        fields = [
            "answer",
        ]"""
    answer = forms.ChoiceField(choices=VALUES, widget=forms.RadioSelect)


class ElectionQuestionFormForm(forms.ModelForm):
    class Meta:
        model = ElectionQuestionForm
        fields = [
            "title"
        ]

class ElectionQuestionCreateForm(forms.ModelForm):
    class Meta:
        model = ElectionQuestion
        fields = [
            "question"
        ]