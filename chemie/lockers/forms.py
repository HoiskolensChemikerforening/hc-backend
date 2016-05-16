from django import forms
from .models import LockerUser, Locker, Ownership
from captcha.fields import ReCaptchaField
from material import *

class RegisterExternalLockerUserForm(forms.ModelForm):
    captcha = ReCaptchaField()
    layout = Layout(Row('first_name', 'last_name'),
                    Row('username'),)
    class Meta:
        model = LockerUser
        fields = [
            "first_name",
            "last_name",
            "username",
        ]

class RegisterInternalLockerUserForm(forms.ModelForm):
    class Meta:
        model = LockerUser
        fields = [
            "internal_user"
        ]
