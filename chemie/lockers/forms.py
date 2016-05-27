from django import forms
from .models import LockerUser
from captcha.fields import ReCaptchaField
import material as M


class RegisterExternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()
    layout = M.Layout(M.Row('first_name', 'last_name'),
                      M.Row('username'),)

    class Meta:
        model = LockerUser
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
