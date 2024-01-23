from django import forms
from .models import Refound
from django.forms import modelformset_factory
from django.core.validators import MinLengthValidator



class DatePickerInput(forms.DateTimeInput):
    input_type = 'date'

class AccountNumberForm(forms.Form):
    account_number = forms.CharField(max_length=11, validators=[MinLengthValidator(11)])

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

