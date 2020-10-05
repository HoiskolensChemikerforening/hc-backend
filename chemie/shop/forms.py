from django import forms
from dal import autocomplete
from .models import Item, Category, RefillReceipt, HappyHour, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class RefillBalanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "receiver", "amount", Submit("submit", "Fyll på konto")
        )

    class Meta:
        model = RefillReceipt
        fields = ["receiver", "amount"]
        widgets = {
            "receiver": autocomplete.ModelSelect2(
                url="verv:user-autocomplete"
            ),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00"}),
        }


class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "name", Submit("submit", "Lagre kategorien")
        )

    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Skriv inn kategorinavn"}
            )
        }


class AddItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "name",
            "price",
            "image",
            Row(
                Column("category", css_class="form-group col-md-6 mb-0"),
                Column(
                    "happy_hour_duplicate",
                    css_class="form-group col-md-6 mb-0",
                ),
                css_class="form-row",
            ),
            "buy_without_tablet",
            Submit("submit", "Lagre varen"),
        )

    class Meta:
        model = Item
        fields = [
            "name",
            "price",
            "category",
            "image",
            "happy_hour_duplicate",
            "buy_without_tablet",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Skriv inn varenavn"}
            ),
            "price": forms.NumberInput(attrs={"placeholder": "0.00"}),
        }


class HappyHourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout("duration")

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
                Column("category", css_class="form-group col-md-6 mb-0"),
                Column(
                    "happy_hour_duplicate",
                    css_class="form-group col-md-6 mb-0",
                ),
                css_class="form-row",
            ),
            "is_active",
            "buy_without_tablet",
            Submit("submit", "Lagre varen"),
        )

    class Meta:
        model = Item
        fields = [
            "name",
            "price",
            "image",
            "category",
            "happy_hour_duplicate",
            "is_active",
            "buy_without_tablet",
        ]


class GetUserRefillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "receiver", Submit("submit", "Hent bruker")
        )

    class Meta:
        model = RefillReceipt
        fields = ["receiver"]
        widgets = {
            "receiver": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }


class GetUserReceiptsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout("buyer", Submit("submit", "Hent bruker"))

    class Meta:
        model = Order
        fields = ["buyer"]
        widgets = {
            "buyer": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }


class SearchItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout("name")
        for k, field in self.fields.items():
            if "required" in field.error_messages:
                field.error_messages["required"] = ""

    class Meta:
        model = Item
        fields = ["name"]
        widgets = {
            "name": autocomplete.ListSelect2(url="shop:item-autocomplete")
        }
