from dataclasses import fields
from django import forms
from .models import Merch, MerchCategory
from dal import autocomplete


class MerchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MerchForm, self).__init__(
            *args, **kwargs
        )  # Call to ModelForm constructor
        self.fields["category"].widget.attrs["style"] = "width:100%;"

    category = forms.ModelChoiceField(
        queryset=MerchCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url="merch:category-autocomplete"),
    )

    layout = [
        [("name", 12)],
        [("price", 12)],
        [("image", 12)],
        [("info", 12)],
        [("category", 12)]
    ]
    

    class Meta:
        model = Merch
        fields = "__all__"


class MerchCategoryForm(forms.ModelForm):

    class Meta:
        model = MerchCategory
        fields = ["name"]


class SortingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SortingForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs["style"] = "width:100%;"

    
    category = forms.ModelChoiceField(
        queryset=MerchCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url="merch:category-autocomplete"),
        label="Kategori",
    )
