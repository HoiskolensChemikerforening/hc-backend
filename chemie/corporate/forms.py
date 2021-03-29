from .models import (
    Interview,
    JobAdvertisement,
    Specialization,
    SurveyQuestion,
    Survey,
    AnswerKeyValuePair,
)
from django import forms
from django.shortcuts import get_object_or_404


class InterviewForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Aktuelle retninger",
    )

    class Meta:
        model = Interview
        fields = ["title", "text", "picture", "specializations"]


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement
        fields = ["title", "description"]


class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = "__all__"


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = "__all__"


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerKeyValuePair
        fields = "__all__"


class AddQuestionToSurveyForm(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        super(AddQuestionToSurveyForm, self).__init__(*args, **kwargs)
        self.fields["questions"].choices = choices

    questions = forms.MultipleChoiceField(
        choices=(),
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "custom-checkboxes"}
        ),
    )
