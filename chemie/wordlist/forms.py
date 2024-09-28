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
        fields = "__all__"




class NounInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("word"),
        M.Row("definite_singular"),
        M.Row("indefinite_plural"),
        M.Row("definite_plural"),
        
    )
    
    class Meta:
        model = Noun 
        fields = "__all__"
        
    



class VerbInput(forms.ModelForm):

    layout = M.Layout(
        M.Row("word"),
        M.Row("present"),
        M.Row("past"),
        M.Row("future"),
        
    )

    class Meta:
        model = Verb 
        fields = "__all__"
        

class AdjectiveInput(forms.ModelForm):

    layout = M.Layout(
    M.Row("word"),
        M.Row("comparative"),
        M.Row("superlative"),
        
    )

    class Meta:
        model = Adjective 
        fields = "__all__"
        




class WordSearchMainPage(forms.Form):
    the_word = forms.CharField(max_length=120, required=False)




class CategorySortingMainPage(forms.Form):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), required=False, label = False)




class CategoryInput(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"




class CheckWhatFormForm(forms.Form):
    choice = forms.ChoiceField(queryset = ["Et annet type ord", "Verb", "Substantiv", "Adjektiv"], label = False, required=True)