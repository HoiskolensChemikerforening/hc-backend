from django import forms
from .models import CGP, Group, Country, CgpPosition


class CGPForm(forms.ModelForm):
    class Meta:
        model = CGP
        fields = ()


class GroupForm(forms.ModelForm):
    """
    """
    country = forms.ModelChoiceField(queryset=None)
    def __init__(self, cgp, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        groups = cgp.group_set.all()
        self.fields['country'].queryset = Country.objects.exclude(group__in=groups)

    class Meta:
        model = Group
        fields = ("__all__")
        exclude = ("cgp","has_voted",)

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("__all__")
        exclude = ("slug", )

class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = CgpPosition
        fields = ("__all__")
        exclude = ("group",)