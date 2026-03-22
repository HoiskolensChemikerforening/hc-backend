from django import forms
import material as M
from .models import Submission


class PostForm(forms.ModelForm):
    layout = M.Layout(M.Row("content"), M.Row("image"))

    class Meta:
        model = Submission
        fields = ["content", "image"]
