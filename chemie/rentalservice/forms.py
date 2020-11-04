from django import forms
import material as M
from .models import RentalObject


class RentalObjectForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("name"), M.Row("description"), M.Row("image"), M.Row("owner")
    )

    class Meta:
        model = RentalObject
        fields = ["name", "description", "image", "owner"]
