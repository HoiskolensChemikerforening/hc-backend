from django import forms
import material as M
from .models import Article
from django.template.defaultfilters import slugify

class NewsForm(forms.ModelForm):

    layout = M.Layout(M.Row('title'),
                      M.Row('content'),
                      M.Row('image'))
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "image"
        ]

    def clean(self):
        super(NewsForm, self).clean()
        self.cleaned_data['slug'] = slugify(self.cleaned_data['slug'])
