from django import forms
from .models import Word, Category



class WordInput(forms.ModelForm):

    class Meta:
        model = Word
        fields = ["word", "explanations", "picture", "secret", "category"]




class WordSearchMainPage(forms.Form):
    the_word = forms.CharField(max_length=120, required=False)




class CategorySortingMainPage(forms.Form):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label='Car Type', required=False)

