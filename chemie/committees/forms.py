from django import forms

from .models import Member, Committee, Position
from dal import autocomplete


class EditCommittees(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'committee',
            'position',
            'user',
        ]
        widgets = {
            'user': autocomplete.ModelSelect2(url='user-autocomplete')
                   }
