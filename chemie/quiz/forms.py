from django import forms
from .models import QuizScore
from dal import autocomplete


class QuizScoreForm(forms.ModelForm):
    class Meta:
        model = QuizScore
        fields = ['user', 'score']
        widgets = {
            'user': autocomplete.ModelSelect2(
                url="verv:user-autocomplete"
            ),
        }
