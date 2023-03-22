from django import forms

class StocktypeForm(forms.Form):
    name = forms.CharField(label = "Stock name", max_length= 30)
    desc = forms.CharField(label = "Stock description", widget=forms.Textarea, max_length= 1000)
    amount = forms.IntegerField(label = "Amount", max_value= 10000)
