from django import forms
from .models import RentalObject, RentalObjectType, Invoice
from django.core.exceptions import ValidationError

CREATE_TYPE_CHOICES = (
    (0, "Bruk eksisterende produkttype"),
    (1, "Legg til ny produkttype"),
)


class RentalObjectForm(forms.ModelForm):
    class Meta:
        model = RentalObject
        fields = [
            "name",
            "description",
            "price",
            "type",
            "quantity",
            "image",
        ]


class CreateRentalObjectForm(RentalObjectForm):
    is_new_type = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=CREATE_TYPE_CHOICES,
        initial=0,
        label="",
    )

    new_type_name = forms.CharField(
        max_length=100, required=False, label="Ny produkttype"
    )
    description = forms.CharField(widget=forms.Textarea,label="Beskrivelse",required=True)

    layout = [
            [("name",12)],
            [("description",12)],
            #[("price",6),("quantity",6)],
            #[("is_new_type",12)],
            #[("type",6),("new_type_name",6)],
            [("image",12)]
            ]


    # def clean(self):
    #    self.cleaned_data["is_new_type"] = bool(int(self.data["is_new_type"]))
    #    super(CreateRentalObjectForm, self).clean()
    #    if not self.is_valid:
    #        return

    #    if self.cleaned_data["is_new_type"]:
    #        if RentalObjectType.objects.filter(
    #            type=self.cleaned_data["new_type_name"]
    #        ):
    #            raise ValidationError("Produkttypen finnes allerede")
    #       new_type = RentalObjectType(
    #            type=self.cleaned_data["new_type_name"]
    #        )
    #        new_type.save()
    #        self.cleaned_data["type"] = new_type

    class Meta(RentalObjectForm.Meta):
        fields = RentalObjectForm.Meta.fields + [
            "is_new_type",
            "new_type_name",
        ]


class InvoiceForm(forms.ModelForm):
    layout = [
                [("event",12)],
                [("client",12)],
                [("client_mail",12)],
                [("client_phone_nr",12)]
                ]
    


    class Meta:
        model = Invoice
        fields = ["event", "client", "client_mail", "client_phone_nr"]


class TypeForm(forms.ModelForm):

    class Meta:
        model = RentalObjectType
        fields = ["type"]
