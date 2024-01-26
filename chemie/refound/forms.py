from django import forms
from .models import Refound, RefoundRequest
from django.forms import modelformset_factory
from django.core.validators import MinLengthValidator



class DatePickerInput(forms.DateTimeInput):
    input_type = 'date'

class AccountNumberForm(forms.ModelForm):
    #account_number = forms.CharField(max_length=11, validators=[MinLengthValidator(11)])
    class Meta:
        model = RefoundRequest
        fields = ["account_number"]
        widgets = {
            'account_number': forms.TextInput({'placeholder': 'Oppgi elleve sifre uten punktum (.)'})
        }

class RefoundForm(forms.ModelForm):
    class Meta:
        model = Refound
        fields = ["date", "store", "item", "event", "price", "image"]
        widgets = {
            "date": DatePickerInput()
        }

RefoundFormSet = modelformset_factory(
    Refound, fields=["date", "store", "item", "event", "price", "image"],widgets = {
            "date": DatePickerInput()
        }, extra=1
)

