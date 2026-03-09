from django import forms
from .models import Role, Scheme, Member, Investment
from chemie.customprofile.models import Profile
from django.forms import modelformset_factory, BaseModelFormSet




class RoleForm(forms.ModelForm):
    
    class Meta:
        model = Role 
        fields = "__all__"


class SchemeForm(forms.ModelForm):
    
    class Meta:
        model = Scheme
        fields = "__all__"


class MemberForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = "__all__"


class InverstmentForm(forms.ModelForm):
    
    class Meta:
        model = Investment
        fields = "__all__"
