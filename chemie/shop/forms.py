from django import forms
from dal import autocomplete
from django.contrib.auth.models import User
import material as M


class RefillBalanceForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url="verv:user-autocomplete"),
    )
    amount = forms.DecimalField(max_digits=6, decimal_places=2)

    layout = M.Layout(M.Row("Bruker"), M.Row("Beløp"))
