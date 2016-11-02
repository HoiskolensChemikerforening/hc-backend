from django import forms
from django.contrib.auth.models import User


#class NameSearchForm(forms.Form):
#    search_field = forms.CharField(label=' ', max_length=100)


class NameSearchForm(forms.Form):
    search_field = forms.CharField(max_length=120)