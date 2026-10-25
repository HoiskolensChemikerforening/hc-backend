
from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from .models import FundsApplication
from .models import OfficeApplication


class ContactForm(forms.Form):
    layout = [
                [("contact_name", 6), ("contact_email", 6)],
                [("content", 12)],
                [("captcha", 12)]
            ]

    field_icons = {
            "contact_name": "account_circle",
            "contact_email": "contact_mail",
            "content": "message"
        }

    captcha = ReCaptchaField()
    contact_name = forms.CharField(required=False, label="Navn")
    contact_email = forms.EmailField(required=False, label="E-post")
    content = forms.CharField(
        required=True, widget=forms.Textarea, label="Melding"
    )


class PostFundsForm(forms.ModelForm):
    layout = [
                [("applier", 6), ("bank_account_holder", 6)],
                [("price_range", 6), ("bank_account_id", 6)],
                [("purpose", 12)],
                [("description", 12)]
            ]

    field_icons = {
        "applier": "recent_actors",
        "bank_account_holder": "assignment_ind",
        "price_range": "shopping_cart",
        "bank_account_id": "play_for_work",
        "purpose": "label",
        "description": "description",
    }


    class Meta:
        model = FundsApplication
        widgets = {
            "price_range": forms.RadioSelect,
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Beskrivelse av formålet, dato, hvor, hvor mye midler det søkes på."
                }
            ),
            "purpose": forms.TextInput(
                attrs={
                    "placeholder": "Kort beskrivelse av det det søkes midler til"
                }
            ),
        }

        fields = [
            "applier",
            "bank_account_holder",
            "price_range",
            "bank_account_id",
            "purpose",
            "description",
        ]


class PostOfficeForms(forms.ModelForm):
    class Meta:
        model = OfficeApplication
        fields = ["student_username"]


class FlatpageEditForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name="flatpages"))

    class Meta:
        model = FlatPage
        fields = ("content",)


class ApprovedTermsForm(forms.Form):
    approval = forms.BooleanField(
        required=True,
        label="Jeg godkjenner ",
        validators=[lambda x: x == True],
    )
