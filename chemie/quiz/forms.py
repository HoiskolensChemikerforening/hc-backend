from django import forms
from .models import QuizScore, QuizTerm
from dal import autocomplete


class QuizScoreForm(forms.ModelForm):
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


class CreateQuizTermForm(forms.ModelForm):
    class Meta:
        model = QuizTerm
        fields = ['term', 'is_active']
