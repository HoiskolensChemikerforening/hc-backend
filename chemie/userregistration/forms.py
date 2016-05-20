from django import forms
from django.contrib.auth.models import User
from customprofile.models import Profile, GRADES, YEARS, CURRENT_YEAR, STIPULATED_TIME
from material import *

class RegisterUser(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = confirm_password = forms.CharField(widget=forms.PasswordInput, label ="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label ="Confirm password")
    grade = forms.ChoiceField(choices = GRADES, widget=forms.Select(), label='')

    layout = Layout(Row('username'),Row('first_name', 'last_name'), Row('password','confirm_password'), Row('grade'))

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    grade = forms.ChoiceField(choices= GRADES)
    allergies = forms.CharField()
    start_year = forms.ChoiceField(choices =((None, CURRENT_YEAR), ('',YEARS)))
    end_year = forms.ChoiceField(choices =((None, (CURRENT_YEAR+STIPULATED_TIME)), ('',YEARS)))
    phone_number = forms.CharField()
    access_card = forms.CharField()
    image_primary = forms.FileField(label='Profilbilde')
    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Personlige detaljer',
                             Row('first_name', 'last_name'),
                             'grade','start_year','end_year'),Row('allergies'),Row('phone_number', 'access_card'), Row('image_primary'))
