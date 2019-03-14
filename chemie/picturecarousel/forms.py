from django import forms
from dal import autocomplete
from .models import Contribution, PictureTag
import material as M


class Pictureform(forms.ModelForm):
    layout = M.Layout(M.Row('image'),
                      M.Row('tags'))

    class Meta:
        model = Contribution
        fields = ["image",
                  "tags"]

        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='picturecarousel:picturetag-autocomplete',
                attrs={
                    'style': 'width: 10px;'
                }
            )
        }


class PictureTagForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['tags']

        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='picturecarousel:picturetag-autocomplete',
                attrs={
                    'style': 'width: 10px;',
                }
            )
        }

        labels = {
            'tags': ''
        }
