from .models import (
    Interview,
    Job,
    Specialization,
    SurveyQuestion,
    Survey,
    AnswerKeyValuePair,
    PositionType,
)

from django import forms


class InterviewForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Aktuelle retninger",
    )

    class Meta:
        model = Interview
        fields = [
            "title",
            "graduation_year",
            "text",
            "picture",
            "company_picture",
            "specializations",
        ]


class JobForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Aktuelle retninger",
    )

    postype = forms.ModelMultipleChoiceField(
        queryset=PositionType.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Stillingstype",
    )

    class Meta:
        model = Job
        fields = ["title", "description", "specializations", "postype"]


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
