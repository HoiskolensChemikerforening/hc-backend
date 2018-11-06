import material as M
from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from .models import FundsApplication
from .models import OfficeApplication


class ContactForm(forms.Form):
    layout = M.Layout(M.Row('contact_name', 'contact_email'),
                      M.Row('content'),
                      M.Row('captcha')
                      )
    captcha = ReCaptchaField()
    contact_name = forms.CharField(required=False, label="Navn")
    contact_email = forms.EmailField(required=False, label="E-post")
    content = forms.CharField(required=True, widget=forms.Textarea, label="Melding")


class PostFundsForm(forms.ModelForm):
    layout = M.Layout(M.Row('applier', 'bank_account_holder'),
                      M.Row('price_range', 'bank_account_id'),
                      M.Row('purpose'),
                      M.Row('description'),
                      M.Row('receipt'),
                      )

    class Meta:
        model = FundsApplication
        widgets = {'price_range': forms.RadioSelect,
                   'description': forms.Textarea(attrs={
                       'placeholder': 'Beskrivelse av formålet, dato, hvor, hvor mye midler det søkes på, hva pengene skal brukes på, osv.'}),
                   'purpose': forms.TextInput(attrs={'placeholder': 'Kort beskrivelse av det det søkes midler til'})}

        fields = [
            "applier",
            "bank_account_holder",
            "price_range",
            "bank_account_id",
            "purpose",
            "description",
            "receipt",
        ]


class PostOfficeForms(forms.ModelForm):
    class Meta:
        model = OfficeApplication
        fields = ["student_username"]


class FlatpageEditForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='flatpages'))
    class Meta:
        model = FlatPage
        fields = ('content',)
