from django import forms
import material as M
from .models import Word, Category



class WordInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("word"),
        M.Row("explanations"),
        M.Row("picture"),
        M.Row("secret"),
        M.Row("category"),
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Word
        fields = ["word", "explanations", "picture", "secret", "category"]




class WordSearchMainPage(forms.Form):
    the_word = forms.CharField(max_length=120, required=False)




class CategorySortingMainPage(forms.Form):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label='Car Type', required=False)

