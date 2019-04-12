from django import forms
from dal import autocomplete
import material as M
from .models import Item, Category, RefillReceipt, HappyHour
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class RefillBalanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "receiver",
            "amount",
            Submit('submit', 'Lagre varen')
        )

    class Meta:
        model = RefillReceipt
        fields = ["receiver", "amount"]
        widgets = {
            "receiver": autocomplete.ModelSelect2(url="verv:user-autocomplete"),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00"})
        }


class AddCategoryForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"))

    class Meta:
        model = Category
        fields = ["name"]


class AddItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "name",
            "price",
            "image",
            Row(
                Column("category", css_class='form-group col-md-6 mb-0'),
                Column("happy_hour_duplicate", css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Lagre varen')
        )

    class Meta:
        model = Item
        fields = ["name", "price", "category", "image", "happy_hour_duplicate"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Skriv inn varenavn"})
        }


class HappyHourForm(forms.ModelForm):
    layout = M.Layout(M.Row("duration"))

    class Meta:
        model = HappyHour
        fields = ["duration"]


class EditItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "name",
            "price",
            "image",
            Row(
                Column("category", css_class='form-group col-md-6 mb-0'),
                Column("happy_hour_duplicate", css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            "is_active",
            Submit('submit', 'Lagre varen')
        )

    class Meta:
        model = Item
        fields = [
            "name",
            "price",
            "image",
            "category",
            "happy_hour_duplicate",
            "is_active"
        ]
