from django import forms


class NameSearchForm(forms.Form):
    search_field = forms.CharField(max_length=120)
