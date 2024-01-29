from django import forms
from .models import Refound, RefoundRequest
from django.forms import modelformset_factory
from django.core.validators import MinLengthValidator


class DatePickerInput(forms.DateTimeInput):
    """
    Class to add a date picker to the date field.
    """
    input_type = "date"


class AccountNumberForm(forms.ModelForm):
    """
    Form to create a RefoundRequest object.
    """
    class Meta:
        model = RefoundRequest
        fields = ["account_number"]
        widgets = {
            "account_number": forms.TextInput(
                {"placeholder": "Elleve sifre uten punktum (.)"}
            )
        }


class RefoundForm(forms.ModelForm):
    """
    Form to create a Refound object.
    """
    class Meta:
        model = Refound
        fields = ["date", "store", "item", "event", "price", "image"]
        widgets = {"date": DatePickerInput()}

    def __init__(self, *arg, **kwarg):
        """
        Override __init__ to ensure that the form must contain data and can not be submitted empty.
        """
        super(RefoundForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

# Create a formset for the refound object to enable multible refound forms on one page.
RefoundFormSet = modelformset_factory(
    Refound,
    form=RefoundForm,
    extra=1,
)


