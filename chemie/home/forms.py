from django import forms
import material as M
from captcha.fields import ReCaptchaField
from .models import FundsApplicationModel


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
    layout = M.Layout(M.Row('applier','bank_account_holder'),
                      M.Row('price_range','bank_account_id'),
                      M.Row('purpose'),
                      M.Row('description'),
                      M.Row('receipt'),
                      )

    class Meta:
        model = FundsApplicationModel
        widgets = {'price_range': forms.RadioSelect}
        fields = [
            "applier",
            "bank_account_holder",
            "price_range",
            "bank_account_id",
            "purpose",
            "description",
            "receipt",
        ]



