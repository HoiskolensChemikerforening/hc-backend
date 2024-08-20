from django import forms
import material as M
from .models import Word, Category, Noun, Verb, Adjective



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




class NounInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("indefinite_singular"),
        M.Row("definite_singular"),
        M.Row("indefinite_plural"),
        M.Row("definite_plural"),
        
    )
    
    class Meta:
        model = Noun 
        fields = ["indefinite_singular", "indefinite_plural", "definite_singular", "definite_plural"]
        
    



class VerbInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("infinitive"),
        M.Row("present"),
        M.Row("past"),
        M.Row("future"),
        
    )

    class Meta:
        model = Verb 
        fields = ["infinitive", "present", "past", "future"]
        

class AdjectiveInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("positive"),
        M.Row("comparative"),
        M.Row("superlative"),
        
    )

    class Meta:
        model = Adjective 
        fields = ["positive", "comparative", "superlative"]
        




class WordSearchMainPage(forms.Form):
    the_word = forms.CharField(max_length=120, required=False)




class CategorySortingMainPage(forms.Form):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label='Car Type', required=False)

class CategoryInput(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"