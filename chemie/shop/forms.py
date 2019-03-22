from django import forms
from dal import autocomplete
import material as M
from .models import Item, Category, RefillReceipt, HappyHour


class RefillBalanceForm(forms.ModelForm):
    layout = M.Layout(M.Row("receiver"), M.Row("amount"))

    class Meta:
        model = RefillReceipt
        fields = ["receiver", "amount"]
        widgets = {
            "receiver": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }


class AddCategoryForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"))

    class Meta:
        model = Category
        fields = ["name"]


class AddItemForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"), M.Row("price"), M.Row("category"), M.Row("image")
    )

    class Meta:
        model = Item
        fields = ["name", "price", "category", "image"]


class HappyHourForm(forms.ModelForm):
    layout = M.Layout(M.Row("duration"))

    class Meta:
        model = HappyHour
        fields = ["duration"]
