from django import forms
from dal import autocomplete
from .models import QuizScore, QuizTerm


class CreateQuizScoreForm(forms.ModelForm):
    class Meta:
        model = QuizScore
        fields = ['user', 'score']
        widgets = {
            'user': autocomplete.ModelSelect2(
                url="verv:user-autocomplete"
            ),
            'score': forms.NumberInput(
                attrs={
                    'style': 'width:10ch; margin-left: 10px;'
                })
        }


class EditQuizScoreForm(forms.ModelForm):
    class Meta:
        model = QuizScore
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(
                attrs={
                    'style': 'width:10ch; margin-left: 10px;'
                })
        }
        labels = {
            'score': ''
        }


class CreateQuizTermForm(forms.ModelForm):
    class Meta:
        model = QuizTerm
        fields = ['term', 'is_active']
