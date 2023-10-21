from django import forms
from .models import ElectionQuestionForm, ElectionQuestion


class ElectionQuestionFormForm(forms.ModelForm):
    """
    Form to create new ElectionQuestionForm objects.
    """

    class Meta:
        model = ElectionQuestionForm
        fields = ["title", "description"]


class ElectionQuestionCreateForm(forms.ModelForm):
    """
    Form to create new ElectionQuestion objects.
    """

    class Meta:
        model = ElectionQuestion
        fields = ["question"]
