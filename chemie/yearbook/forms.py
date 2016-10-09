from django import forms

class NameSearchForm(forms.Form):
    search_field = forms.CharField(label=' ', max_length=100)