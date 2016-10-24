from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from .models import Profile
import material as M
from django.core.validators import ValidationError

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Passord")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Gjenta passord")

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
        password = self.cleaned_data.get('password')
        confrimed_password = self.cleaned_data.get('password_confirm')


        if not password:
            self.add_error(None, ValidationError({'password':["Feltet er påkrevd"]}))

        if not confrimed_password:
            self.add_error(None, ValidationError({'password_confirm':["Feltet er påkrevd"]}))

        if password != confrimed_password:
            message = 'Password does not match'
            self.add_error(None, ValidationError({'password_confirm':["Passordene stemmer ikke overens"]}))
            return False
        return password

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


class EditUserForm(forms.ModelForm):
    layout = M.Layout(M.Row('first_name', 'last_name'),
                      M.Row('email'))

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                ]

class EditProfileForm(forms.ModelForm):
    layout = M.Layout(M.Row('start_year', 'end_year'),
                      M.Row('address'),
                      M.Row('access_card'),
                      M.Row('phone_number'),
                      M.Row('allergies', 'relationship_status'))
    class Meta:
        model = Profile
        fields = ["start_year",
                  "end_year",
                  "access_card",
                  "phone_number",
                  "allergies",
                  "address",
                  "relationship_status"
                ]
class ChangePasswordForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput, label="Old password")
        password_new = forms.CharField(widget=forms.PasswordInput, label="New password")
        password_new_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")
        layout = M.Layout(M.Row('password'),
                          M.Row('password_new', 'password_new_confirm'),)
        class Meta:
            model = User
            fields = ["password",
            "password_new",
            "password_new_confirm"
            ]

        def password_matches(self):
            password = self.cleaned_data.get('password')
            password_new = self.cleaned_data.get('password_new')
            password_new_confirm = self.cleaned_data.get('password_new_confirm')
            if not password:
                self.add_error(None, ValidationError({'password':["Feltet er påkrevd"]}))
            if not password_new:
                self.add_error(None, ValidationError({'password_new':["Feltet er påkrevd"]}))
            if not password_new_confirm:
                self.add_error(None, ValidationError({'password_new_confirm':["Feltet er påkrevd"]}))
            if password_new != password_new_confirm:
                message = 'Password does not match'
                self.add_error(None, ValidationError({'password_new_confirm':["Passordene stemmer ikke overens"]}))
                return False
            return password_new

        def clean(self):
            super(ChangePasswordForm, self).clean()
            self.password_matches()


class ForgotPassword(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    layout = M.Layout(M.Row('email'))

    class Meta:
        model = User
        fields = ['email']


class SetNewPassword(forms.ModelForm):
    password_new = forms.CharField(widget=forms.PasswordInput, label="New password")
    password_new_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")
    layout = M.Layout(M.Row('password_new'),
                      M.Row('password_new_confirm'))

    class Meta:
        model = User
        fields = ['password_new',
                  'password_new_confirm',
                  ]

    def password_matches(self):
        password_new = self.cleaned_data.get('password_new')
        password_new_confirm = self.cleaned_data.get('password_new_confirm')
        if not password_new:
            self.add_error(None, ValidationError({'password_new': ["Feltet er påkrevd"]}))
        if not password_new_confirm:
            self.add_error(None, ValidationError({'password_new_confirm': ["Feltet er påkrevd"]}))
        if password_new != password_new_confirm:
            self.add_error(None, ValidationError({'password_new_confirm': ["Passordene stemmer ikke overens"]}))
            return False
        return password_new

    def clean(self):
        super(SetNewPassword, self).clean()
        self.password_matches()

