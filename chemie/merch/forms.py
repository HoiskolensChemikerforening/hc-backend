from dataclasses import fields
from django import forms
from .models import Merch, MerchCategory
import material as M
from dal import autocomplete


class MerchForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"), M.Row("price"), M.Row("image"), M.Row("info"), M.Row("category"))

    class Meta:
        model = Merch
        fields = ["name", "price", "image", "info", "category"]
        widgets = {
            "category": autocomplete.ModelSelect2Multiple(
                url="merch:user-autocomplete",
                attrs={"data-maximum-selection-length": 1},
            )
        }

class MerchCategoryForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"))

    class Meta:
        model = MerchCategory
        fields = ["name"]