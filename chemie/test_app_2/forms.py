from django import forms
from .models import Cult
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseModelFormSet



class BookForm(forms.ModelForm):
    
    class Meta:
        model = Cult
        fields = "__all__"
