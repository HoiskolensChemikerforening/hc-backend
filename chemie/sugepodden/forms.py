from .models import Podcast
from django import forms


class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ["title", "description", "url", "image"]
