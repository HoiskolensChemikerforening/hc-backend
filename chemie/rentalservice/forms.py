from django import forms
import material as M
from .models import RentalObject, RentalObjectType, Invoice


class RentalObjectForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"),
        M.Row("description"),
        M.Row("price", "quantity"),
        M.Row("type"),
        M.Row("image"),
        M.Row("owner")
    )

    class Meta:
        model = RentalObject
        widgets = {
        }
        fields = ["name", "description", "price", "type", "quantity", "image", "owner"]


class InvoiceForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("event"), M.Row("client"), M.Row("client_mail"), M.Row("client_nr"), M.Row("paid")
    )

    class Meta:
        model = Invoice
        fields = ["event", "client", "client_mail", "client_nr", "paid"]


class TypeForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("type")
    )

    class Meta:
        model = RentalObjectType
        fields = ["type"]
