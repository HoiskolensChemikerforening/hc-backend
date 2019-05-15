import material as M
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from chemie.chemie.settings import REGISTRATION_KEY
from .models import Profile


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Passord")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Gjenta passord"
    )

    layout = M.Layout(
        M.Row("first_name", "last_name"),
        M.Row("email"),
        M.Row("username"),
        M.Row("password", "password_confirm"),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

    def password_matches(self):
        password = self.cleaned_data.get("password")
        confrimed_password = self.cleaned_data.get("password_confirm")

        if not password:
            self.add_error(
                None, ValidationError({"password": ["Feltet er påkrevd"]})
            )

        if not confrimed_password:
            self.add_error(
                None,
                ValidationError({"password_confirm": ["Feltet er påkrevd"]}),
            )

        if password != confrimed_password:
            message = "Password does not match"  # Redundant?
            self.add_error(
                None,
                ValidationError(
                    {"password_confirm": ["Passordene stemmer ikke overens"]}
                ),
            )
            return False
        return password

    def clean(self):
        super(RegisterUserForm, self).clean()
        self.password_matches()


class RegisterProfileForm(forms.ModelForm):
    #    registration_key = forms.CharField(max_length=40, required=True)
    layout = M.Layout(
        M.Row("grade"),
        M.Row("start_year", "end_year"),
        M.Row("address"),
        M.Row("access_card"),
        M.Row("phone_number"),
        M.Row("allergies", "relationship_status"),
        M.Row("image_primary", "image_secondary"),
    )

    # M.Row('registration_key'),)

    class Meta:
        model = Profile
        fields = [
            "grade",
            "start_year",
            "end_year",
            "access_card",
            "phone_number",
            "allergies",
            "address",
            "relationship_status",
            "image_primary",
            "image_secondary",
        ]

    def not_clean_registration_key(self):
        registration_key = self.cleaned_data.get("registration_key")
        if not registration_key == REGISTRATION_KEY:
            self.add_error(
                None,
                ValidationError(
                    {
                        "registration_key": [
                            "Har du kode eller har du ikke kode? Du må ha kode."
                        ]
                    }
                ),
            )
        return registration_key


class EditUserForm(forms.ModelForm):
    layout = M.Layout(M.Row("first_name", "last_name"), M.Row("email"))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class EditProfileForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("start_year", "end_year"),
        M.Row("address"),
        M.Row("access_card"),
        M.Row("phone_number"),
        M.Row("allergies", "relationship_status"),
    )

    class Meta:
        model = Profile
        fields = [
            "start_year",
            "end_year",
            "access_card",
            "phone_number",
            "allergies",
            "address",
            "relationship_status",
        ]

class EditPushForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'coffee_subscription',
            'news_subscription',
            'happyhour_subscription',
        ]

class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Old password")
    password_new = forms.CharField(
        widget=forms.PasswordInput, label="New password"
    )
    password_new_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm new password"
    )
    layout = M.Layout(
        M.Row("password"), M.Row("password_new", "password_new_confirm")
    )

    class Meta:
        model = User
        fields = ["password", "password_new", "password_new_confirm"]

    def password_matches(self):
        password = self.cleaned_data.get("password")
        password_new = self.cleaned_data.get("password_new")
        password_new_confirm = self.cleaned_data.get("password_new_confirm")
        if not password:
            self.add_error(
                None, ValidationError({"password": ["Feltet er påkrevd"]})
            )
        if not password_new:
            self.add_error(
                None, ValidationError({"password_new": ["Feltet er påkrevd"]})
            )
        if not password_new_confirm:
            self.add_error(
                None,
                ValidationError(
                    {"password_new_confirm": ["Feltet er påkrevd"]}
                ),
            )
        if password_new != password_new_confirm:
            message = "Password does not match"  # Redundant?
            self.add_error(
                None,
                ValidationError(
                    {
                        "password_new_confirm": [
                            "Passordene stemmer ikke overens"
                        ]
                    }
                ),
            )
            return False
        return password_new

    def clean(self):
        super(ChangePasswordForm, self).clean()
        self.password_matches()


class ForgotPassword(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput, label="E-post")
    captcha = ReCaptchaField()
    layout = M.Layout(M.Row("email"), M.Row("captcha"))

    class Meta:
        model = User
        fields = ["email"]


class SetNewPassword(forms.ModelForm):
    password_new = forms.CharField(
        widget=forms.PasswordInput, label="Nytt passord"
    )
    password_new_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Bekreft nytt passord"
    )
    layout = M.Layout(M.Row("password_new"), M.Row("password_new_confirm"))

    class Meta:
        model = User
        fields = ["password_new", "password_new_confirm"]

    def password_matches(self):
        password_new = self.cleaned_data.get("password_new")
        password_new_confirm = self.cleaned_data.get("password_new_confirm")
        if not password_new:
            self.add_error(
                None, ValidationError({"password_new": ["Feltet er påkrevd"]})
            )
        if not password_new_confirm:
            self.add_error(
                None,
                ValidationError(
                    {"password_new_confirm": ["Feltet er påkrevd"]}
                ),
            )
        if password_new != password_new_confirm:
            self.add_error(
                None,
                ValidationError(
                    {
                        "password_new_confirm": [
                            "Passordene stemmer ikke overens"
                        ]
                    }
                ),
            )
            return False
        return password_new

    def clean(self):
        super(SetNewPassword, self).clean()
        self.password_matches()


class NameSearchForm(forms.Form):
    search_field = forms.CharField(max_length=120)


class ApprovedTermsForm(forms.Form):
    approval = forms.BooleanField(
        required=True, label="Jeg godkjenner ", validators=[lambda x: x == True]
    )


class GetRFIDForm(forms.Form):

    rfid = forms.CharField(label='Studentkortnr', max_length=255, widget=forms.NumberInput(attrs={'autofocus': True}))


class AddCardForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='verv:user-autocomplete'))
    access_card = forms.CharField(label='Studentkortnr', max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "Brukernavn",
            "Studentkort",
        )


class ManualRFIDForm(forms.Form):

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='verv:user-autocomplete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "Brukernavn",
        )
