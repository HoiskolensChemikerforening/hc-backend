from django import forms
from .models import Word, Category



class WordInput(forms.ModelForm):

    class Meta:
        model = Word
        fields = ["word", "explanations", "picture", "secret", "category"]




class CategorySortingMainPage(forms.Modelform):

    class Meta:
        model = Category
        fields = ["typeOfWord"]

