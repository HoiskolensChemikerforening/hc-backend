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
        M.Row("name"),
        M.Row("price"),
        M.Row("category"),
        M.Row("image"),
        M.Row("happy_hour_duplicate"),
    )

    class Meta:
        model = Item
        fields = ["name", "price", "category", "image", "happy_hour_duplicate"]


class HappyHourForm(forms.ModelForm):
    layout = M.Layout(M.Row("duration"))

    class Meta:
        model = HappyHour
        fields = ["duration"]


class EditItemForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"),
        M.Row("price"),
        M.Row("category"),
        M.Row("image"),
        M.Row("is_active"),
    )

    class Meta:
        model = Item
        fields = ["name", "price", "category", "image", "is_active"]

    def __init__(self, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
