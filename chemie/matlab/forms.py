from django import forms
from .models import Recipes, Ingredients, KATEGORIER, ALLERGIES
from crispy_forms.layout import Layout
from django.core.validators import ValidationError
import material as M

class IngredientForm(forms.ModelForm):
     class Meta:
        model = Ingredients
        abstract = True
        fields = ["name"]

class RegisterIngredientForm(IngredientForm):
    layout = M.Layout(M.Row("name"))

class RecipesForm(forms.ModelForm):
    allowed_allergies = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ALLERGIES,
        label="Huk av allergier",
    )
    def clean_allowed_allergies(self):
        try:
            allergies = self.cleaned_data.get("allowed_allergies")
            allergies = [int(allergies) for allergie in allergies]
            # Next line checks whether the integers in "grades" corresponds to a choice in GRADES,
            # if not, an exception occurs
            _ = [ALLERGIES.values[int(allergies)] for allergie in allergies]
            return allergies
        except (ValueError, KeyError):
            self.add_error(
                None,
                ValidationError(
                    {
                        "allowed_allergies": [
                            "Allergi ikke akseptert"
                        ]
                    }
                ),
            )
    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=KATEGORIER,
        label="Kategori huk av",
    )
    def clean_categories(self):
        try:
            categories = self.cleaned_data.get("categories")
            categories = [int(categories) for categorie in categories]
            # Next line checks whether the integers in "grades" corresponds to a choice in GRADES,
            # if not, an exception occurs
            _ = [KATEGORIER.values[int(categories)] for categorie in categories]
            return categories
        except (ValueError, KeyError):
            self.add_error(
                None,
                ValidationError(
                    {
                        "categories": [
                            "Kategori ikke akseptert"
                        ]
                    }
                ),
            )
    ingredients = forms.ModelMultipleChoiceField(
            queryset=Ingredients.objects.all(),
            widget=forms.SelectMultiple(),
            required=True,
            label='Ingredients',
        )
    class Meta:
        model = Recipes
        abstract = True
        fields = ["title",
            "ingredients",
            "ingredient_quantity",
            "description",
            "expected_price",
            "portions",
            "time",
            "image",
            "categories",
            "allowed_allergies",
            ]
        
class RegisterRecipiesForm(RecipesForm):
        layout = M.Layout(
        M.Row("title"),
        M.Row(
             M.Column("ingredients"),
             M.Column("ingredient_quantity")
        ),
        M.Row("description"),
        M.Row(
             M.Column("expected_price"),
             M.Column("portions"),
             M.Column("time")
            ),
        M.Row("image"), 
        M.Row("categories"),
        M.Row("allowed_allergies"),

    )