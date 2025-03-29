from django import forms
from .models import Recipes, Ingredients, Kategori, ALLERGIES
from crispy_forms.layout import Layout

class RecipesForm(forms.ModelForm):
    allowed_allergies = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ALLERGIES,
        label="Huk av allergier",
    )
    class Meta:
        model = Ingredients
        model = Kategori
        fields = ["name"]