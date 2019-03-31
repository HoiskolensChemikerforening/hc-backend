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
        widgets = {
            'is_active': forms.CheckboxInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        term = cleaned_data.get('term')
        is_active = cleaned_data.get('is_active')

        if term and is_active:
            active_quiz = QuizTerm.objects.get(is_active=True)
            if active_quiz:
                raise forms.ValidationError(
                    "Det finnes allerede en aktiv Quiz: %s. "
                    "Deaktiver den før du oppretter en ny" % active_quiz.term
                )
