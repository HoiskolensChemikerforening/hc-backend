from django import forms
import material as M
from .models import RentalObject, Invoice


class RentalObjectForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"), M.Row("description"), M.Row("image"), M.Row("owner")
    )

    class Meta:
        model = RentalObject
        fields = ["name", "description", "image", "owner"]


class InvoiceForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("event"), M.Row("client"), M.Row("client_mail"), M.Row("client_nr"), M.Row("paid")
    )

    class Meta:
        model = Invoice
        fields = ["event", "client", "client_mail", "client_nr", "paid"]
