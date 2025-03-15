from django import forms
from .models import Recipes, Ingredients
from crispy_forms.layout import Layout

class RecipesForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ["name"]