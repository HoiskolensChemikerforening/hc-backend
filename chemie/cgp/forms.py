from django import forms
from .models import CGP, Group, Country


class CGPForm(forms.ModelForm):
    class Meta:
        model = CGP
        fields = ()


class GroupForm(forms.ModelForm):
    """
    Todo only show only availible countries
    """
    class Meta:
        model = Group
        fields = ("__all__")
        exclude = ("cgp","has_voted",)

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("country_name", "image")