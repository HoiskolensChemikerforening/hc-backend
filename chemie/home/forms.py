from django import forms
import material as M
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    layout = M.Layout(M.Row('contact_name', 'contact_email'),
                      M.Row('content'),
                      M.Row('captcha')
                      )
    captcha = ReCaptchaField()
    contact_name = forms.CharField(required=False, label="Navn")
    contact_email = forms.EmailField(required=False, label="E-post")
    content = forms.CharField(required=True, widget=forms.Textarea, label="Melding")

