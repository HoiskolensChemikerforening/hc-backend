from django import forms
from dal import autocomplete
from django.contrib.auth.models import User
import material as M
from .models import Item, Category


class RefillBalanceForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url="verv:user-autocomplete"),
    )
    amount = forms.DecimalField(max_digits=6, decimal_places=2)

    layout = M.Layout(M.Row("Bruker"), M.Row("Beløp"))


class AddCategoryForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"))

    class Meta:
        model = Category
        fields = ["name"]


class AddItemForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"),
        M.Row("price"),
        M.Row("description"),
        M.Row("category"),
        M.Row("image"),
    )

    class Meta:
        model = Item
        fields = ["name", "price", "description", "category", "image"]
