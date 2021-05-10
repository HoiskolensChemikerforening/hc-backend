from django import forms
from .models import Merch
import material as M

class MerchForm(forms.ModelForm):
    layout = M.Layout(M.Row("name"), M.Row("price"), M.Row("image"), M.Row("info"))

    class Meta:
        model = Merch
        fields = ["name", "price", "image", "info"]