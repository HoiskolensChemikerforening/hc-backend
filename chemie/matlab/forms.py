from django import forms
from .models import Recipes, KATEGORIER, ALLERGIES
from crispy_forms.layout import Layout
from django.core.validators import ValidationError
import material as M


class RecipesForm(forms.ModelForm):
    allowed_allergies = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ALLERGIES,
        label="Huk av allergier",
    )
    def clean_allowed_allergies(self):
        try:
            allergies = self.cleaned_data.get("allowed_allergies")
            allergies = [int(allergi) for allergi in allergies]
            # Next line checks whether the integers in "grades" corresponds to a choice in GRADES,
            # if not, an exception occurs
            _ = [ALLERGIES.values[int(allergi)] for allergi in allergies]
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
            categories = [int(kategori) for kategori in categories]
            # Next line checks whether the integers in "grades" corresponds to a choice in GRADES,
            # if not, an exception occurs
            _ = [KATEGORIER.values[int(kategori)] for kategori in categories]
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

    class Meta:
        model = Recipes
        fields = ["title",
            "ingredients",
            "description",
            "expected_price",
            "portions",
            "time",
            "image",
            "categories",
            "allowed_allergies"
            ]
        
class RegisterRecipiesForm(RecipesForm):
        layout = M.Layout(
        M.Row("title"),
        M.Row(
             M.Column("ingredients"),
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