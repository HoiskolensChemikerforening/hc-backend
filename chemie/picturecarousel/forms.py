from django import forms
from dal import autocomplete
from .models import Contribution
import material as M


class Pictureform(forms.ModelForm):
    layout = M.Layout(M.Row("image"), M.Row("tagged_users"))

    class Meta:
        model = Contribution
        fields = ["image", "tagged_users"]

        widgets = {
            "tagged_users": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete"
            )
        }

        labels = {"image": "Bilde", "tagged_users": "Personer"}
