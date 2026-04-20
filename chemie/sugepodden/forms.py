from .models import Podcast
from django import forms
import chemie.custommaterial as M


class PodcastForm(forms.ModelForm):
    layout = M.Layout(
        M.Row("title"), M.Row("description"), M.Row("url"), M.Row("image")
    )

    class Meta:
        model = Podcast
        fields = ["title", "description", "url", "image"]
