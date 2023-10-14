from django import forms
from .models import ElectionQuestionForm, ElectionQuestion


class ElectionQuestionFormForm(forms.ModelForm):
    class Meta:
        model = ElectionQuestionForm
        fields = ["title", "description"]


class ElectionQuestionCreateForm(forms.ModelForm):
    class Meta:
        model = ElectionQuestion
        fields = ["question"]
