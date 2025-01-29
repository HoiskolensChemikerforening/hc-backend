from django import forms
from .models import Refund, RefundRequest
from django.forms import modelformset_factory
from django.core.validators import MinLengthValidator


class DatePickerInput(forms.DateTimeInput):
    """
    Class to add a date picker to the date field.
    """

    input_type = "date"


class AccountNumberForm(forms.ModelForm):
    """
    Form to create a RefundRequest object.
    """

    class Meta:
        model = RefundRequest
        fields = ["account_number"]
        widgets = {
            "account_number": forms.TextInput(
                {"placeholder": "Elleve sifre uten punktum (.)"}
            )
        }


class RefundForm(forms.ModelForm):
    """
    Form to create a Refund object.
    """

    class Meta:
        model = Refund
        fields = ["date", "store", "item", "event", "price", "image"]
        widgets = {"date": DatePickerInput()}

    def __init__(self, *arg, **kwarg):
        """
        Override __init__ to ensure that the form must contain data and can not be submitted empty.
        """
        super(RefundForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


# Create a formset for the refund object to enable multible refund forms on one page.

RefundFormSet = modelformset_factory(Refund, form=RefundForm, extra=1)

