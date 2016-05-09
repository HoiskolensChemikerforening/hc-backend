from django import forms
from .models import LockerUser, Locker, Ownership
from captcha.fields import ReCaptchaField


class RegisterExternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = LockerUser
        fields = [
            "first_name",
            "last_name",
            "username",
        ]

class RegisterInternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = LockerUser
        fields = [
            "internal_user"
        ]

