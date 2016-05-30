from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from .models import Profile
import material as M


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    layout = M.Layout(M.Row('first_name', 'last_name'),
                      M.Row('email'),
                      M.Row('username'),
                      M.Row('password', 'password_confirm'),)

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                  "username",
                ]

    def password_matches(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            message = 'Password does not match'
            self.add_error('password', message)
            self.add_error('password_confirm', message)
            return False
        return self.cleaned_data['password']

    def clean(self):
        super(RegisterUserForm, self).clean()
        self.password_matches()


class RegisterProfileForm(forms.ModelForm):
    layout = M.Layout(M.Row('grade'),
                      M.Row('start_year', 'end_year'),
                      M.Row('address'),
                      M.Row('access_card'),
                      M.Row('phone_number'),
                      M.Row('allergies', 'relationship_status'))

    class Meta:
        model = Profile
        fields = ["grade",
                  "start_year",
                  "end_year",
                  "access_card",
                  "phone_number",
                  "allergies",
                  "address",
                  "relationship_status"
                ]
