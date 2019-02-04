from dal import autocomplete
from django import forms
from django.core.validators import ValidationError

from .models import Committee, Position


class EditDescription(forms.ModelForm):
    class Meta:
        model = Committee
        fields = ["description", "one_liner", "image"]


class EditPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("users",)
        widgets = {
            "users": autocomplete.ModelSelect2Multiple(
                url="verv:user-autocomplete",
                attrs={"data-maximum-selection-length": 1},
            )
        }

    def clean(self):
        super(EditPositionForm, self).clean()
        maximum = self.instance.max_members
        if self.cleaned_data.get("users").count() > maximum:
            self.add_error(
                None,
                ValidationError(
                    {
                        "users": [
                            "Stillingen har maksimalt {} personer".format(
                                maximum
                            )
                        ]
                    }
                ),
            )
