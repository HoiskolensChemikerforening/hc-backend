from django import forms
from .models import Disease, Villsvin, Korv
from crispy_forms.layout import Layout, Row
import material as M

class VillsvinForm(forms.ModelForm):
    """
    layout = M.Layout(
        M.Row("name"),
        M.Row("age"),
        M.Row('disease'),
    )"
    """
    class Meta:
        model = Disease
        fields = ["navn", "life_expectancy"]
