from django import forms
from .models import Contribution
import material as M


class Pictureform(forms.ModelForm):
    layout = M.Layout(M.Row("image"))

    class Meta:
        model = Contribution
        fields = ["image"]
