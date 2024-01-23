from django import forms
from .models import Refound
import material as M
from django.forms import modelformset_factory




class DatePickerInput(forms.DateTimeInput):
    input_type = 'date'

class RefoundForm(forms.ModelForm):
    layout = M.Layout(
        M.Row(
            M.Column("date", span_columns=1),

            M.Column("store", span_columns=1)
        ),
        M.Row("item"),
        M.Row(M.Column("event"), M.Column("price")),
        M.Row("image"),
    )
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

