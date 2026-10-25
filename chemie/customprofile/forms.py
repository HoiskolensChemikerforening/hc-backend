
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from chemie.chemie.settings import REGISTRATION_KEY
from .models import Profile, Medal
from chemie.web_push.models import Subscription


class RegisterUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    password = forms.CharField(widget=forms.PasswordInput, label="Passord")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Gjenta passord"
    )

    layout = [
        [("first_name",6), ("last_name",6)],
        [("email",12)],
        [("username",12)],
        [("password",6), ("password_confirm",6)],
    ]

    field_icons = {
            "first_name": "account_circle",
            "last_name": "account_circle",
            "email": "contact_mail"
        }

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


    layout = [
            [("grade",12)],
            [("start_year",6), ("end_year",6)],
            [("specialization",12)],
            [("address",12)],
            [("access_card",12)],
            [("phone_number",12)],
            [("allergies",6), ("relationship_status",6)],
            [("image_primary",6), ("image_secondary",6)],
        ]

    field_icons = {
                "address": "home",
                "access_card": "credit_card",
                "phone_number": "contact_phone",
                "allergies": "error_outline"
            }

    # M.Row('registration_key'),)

    class Meta:
        model = Profile
        fields = [
            "grade",
            "start_year",
            "end_year",
            "specialization",
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
    field_icons = {
        "first_name": "account_circle",
        "last_name": "account_circle",
        "email": "contact_mail"
    }

    layout = [
            
            [("first_name",6),("last_name",6)],
            [("email",12)],
        ] 

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class EditProfileForm(forms.ModelForm):

    field_icons = {
            "address": "home",
            "access_card": "credit_card",
            "phone_number": "contact_phone",
            "allergies": "error_outline"
        }

    layout = [
        [("start_year",6), ("end_year",6)],
        [("address",12)],
        [("specialization",12)],
        [("access_card",12)],
        [("phone_number",12)],
        [("allergies",6), ("relationship_status",6)],
        [("medals",12)],
    ]

    class Meta:
        model = Profile
        fields = [
            "start_year",
            "end_year",
            "specialization",
            "access_card",
            "phone_number",
            "allergies",
            "address",
            "relationship_status",
            "medals",
        ]


class EditPushForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("subscriptions",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(EditPushForm, self).__init__(*args, **kwargs)
        self.fields[
            "subscriptions"
        ].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["subscriptions"].help_text = ""
        self.fields["subscriptions"].queryset = Subscription.objects.filter(
            owner=user
        ).order_by("id")


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Old password"
    )
    password_new = forms.CharField(
        widget=forms.PasswordInput, label="New password"
    )
    password_new_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm new password"
    )
    layout = [
        [("password",12)],
        [("password_new",6),("password_new_confirm",6)],
    ] 

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


class EndYearForm(forms.Form):
    integer_field = forms.IntegerField()


class ApprovedTermsForm(forms.Form):
    approval = forms.BooleanField(
        required=True,
        label="Jeg godkjenner ",
        validators=[lambda x: x == True],
    )


class GetRFIDForm(forms.Form):
    rfid = forms.CharField(
        label="Studentkortnr",
        max_length=255,
        widget=forms.NumberInput(attrs={"autofocus": True}),
    )


class AddCardForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url="verv:user-autocomplete"),
    )
    access_card = forms.CharField(label="Studentkortnr", max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("Brukernavn", "Studentkort")


class ManualRFIDForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url="verv:user-autocomplete"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("Brukernavn")
