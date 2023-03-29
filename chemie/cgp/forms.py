from django import forms
from .models import CGP, ExtraVote


class ExtraPrize(forms.ModelForm):
    vote = forms.ModelChoiceField(queryset=CGP.get_latest_active().group_set.all())
    class Meta:
        model = ExtraVote
        fields = ["vote"]