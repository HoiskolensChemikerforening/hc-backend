from django import forms
from .models import Villsvin, Sykdom
from crispy_forms.layout import Layout

# layout = M.Layout(
#         M.Row("name"),
#         M.Row("age"),
#         M.Row("disease"),
#     )
class VillsvinForm(forms.ModelForm):

    class Meta:
        model = Sykdom
        fields = ["disease_name", "life_expectancy"]