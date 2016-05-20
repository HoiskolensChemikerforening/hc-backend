from django import forms
from django.contrib.auth.models import User
from .models import Profile, GRADES, YEARS, CURRENT_YEAR, STIPULATED_TIME
import material as M


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    layout = M.Layout(M.Row('first_name', 'last_name'),
                      M.Row('username'),
                      M.Row('email'),
                      M.Row('password', 'password_confirm'),)

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                  "username",
                ]


class RegisterProfileForm(forms.ModelForm):
    layout = M.Layout(M.Row('user'),
                      M.Row('grade'),
                      M.Row('start_year', 'end_year'),
                      M.Row('access_card'),
                      M.Row('phone_number'),
                      M.Row('allergies'),
                      M.Row('image_primary'))

    class Meta:
        model = Profile
        fields = ["user",
                  "grade",
                  "start_year",
                  "end_year",
                  "access_card",
                  "phone_number",
                  "allergies",
                  "address",
                  "image_primary",
                ]
