from django import forms
from .models import Book
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseModelFormSet



class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = "__all__"
