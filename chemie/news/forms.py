from django import forms
import chemie.custommaterial as M
from .models import Article


class ArticleForm(forms.ModelForm):
    layout = M.Layout(M.Row("title"), M.Row("content"), M.Row("image"))

    class Meta:
        model = Article
        fields = ["title", "content", "image"]
