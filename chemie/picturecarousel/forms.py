from django import forms
from dal import autocomplete
from .models import Contribution



class Pictureform(forms.ModelForm):

    

    class Meta:
        model = Contribution
        fields = ["image", "tagged_users"]

        widgets = {
            "tagged_users": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete"
            )
        }

        labels = {"image": "Bilde", "tagged_users": "Personer"}


class TagForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ["tagged_users"]

        widgets = {
            "tagged_users": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete"
            )
        }

        labels = {"tagged_users": ""}
