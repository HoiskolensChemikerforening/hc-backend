from django import forms
from .models import LockerUser, Locker, Ownership


class RegisterExternalLockerUserForm(forms.ModelForm):
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

