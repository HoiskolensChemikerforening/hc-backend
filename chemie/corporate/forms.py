from .models import Company
from django import forms


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description", "logo", "specializations"]
