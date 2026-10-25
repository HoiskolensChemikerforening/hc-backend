from django import forms
from .models import LockerUser
from captcha.fields import ReCaptchaField



class RegisterExternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Jeg har lest og godtar brukervilkårene for bruk av bokskap",
    )

    layout = [
        [("first_name",6),("last_name",6)],
        [("email",12)],
        [("agree_to_terms",12)],
    ]

    field_icons = {
            "first_name": "account_circle",
            "last_name": "account_circle",
            "email": "email"
        }

    class Meta:
        model = LockerUser
        fields = ["first_name", "last_name", "email", "agree_to_terms"]


class MyLockersForm(forms.Form):
    email = forms.EmailField()
    layout = [[("email",12)]]


class ConfirmOwnershipForm(forms.Form):
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Jeg har lest og godtar brukervilkårene for bruk av bokskap",
    )
