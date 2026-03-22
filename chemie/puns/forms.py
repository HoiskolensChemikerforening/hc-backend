from django import forms
import material as M
from .models import Puns_Submission


class PostForm(forms.ModelForm):
    layout = M.Layout(M.Row("content"))

    class Meta:
        model = Puns_Submission
        fields = ["content"]
