from dataclasses import fields
from django import forms
from .models import Merch, MerchCategory
import material as M
from dal import autocomplete


class MerchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MerchForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['category'].widget.attrs['style'] = 'width:100%;'

    category = forms.ModelChoiceField(
        queryset=MerchCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='merch:category-autocomplete',),
    )

    layout = M.Layout(M.Row("name"), M.Row("price"), M.Row("image"), M.Row("info"), M.Row("category"))
    class Meta:
        model = Merch
        fields = ("__all__")


class MerchCategoryForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"))

    class Meta:
        model = MerchCategory
        fields = ["name"]


class SortingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SortingForm, self).__init__(*args, **kwargs)
        #self.fields["category"].queryset = MerchCategory.objects.all()
        self.fields['category'].widget.attrs['style'] = 'width:100%;'
    layout = M.Layout(M.Row("category"))
    category = forms.ModelChoiceField(
        queryset=MerchCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='merch:category-autocomplete',),
    )


