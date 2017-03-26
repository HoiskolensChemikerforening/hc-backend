from django import forms
from .models import LockerUser
from captcha.fields import ReCaptchaField
import material as M


class RegisterExternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()
    layout = M.Layout(M.Row('first_name', 'last_name'),
                      M.Row('email'),)

    class Meta:
        model = LockerUser
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class MyLockersForm(forms.Form):
    email = forms.EmailField()
    layout = M.Layout(M.Row('email'),)


class ConfirmOwnershipForm(forms.Form):
    agree_to_terms = forms.BooleanField(required=True, label='Jeg har lest og godtar brukervilkårene for bruk av bokskap')
