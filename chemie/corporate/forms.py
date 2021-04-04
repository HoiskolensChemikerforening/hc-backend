from .models import Interview, JobAdvertisement, Specialization
from django import forms


class InterviewForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Aktuelle retninger",
    )

    class Meta:
        model = Interview
        fields = ["title", "graduation_year", "text", "picture", "company_picture", "specializations"]


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement
        fields = ["title", "description"]
