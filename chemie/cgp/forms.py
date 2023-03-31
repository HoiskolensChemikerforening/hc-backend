from django import forms
from .models import Group, Country


class GroupForm(forms.ModelForm):
    """
    """
    country = forms.ModelChoiceField(queryset=None, label='Land')
    def __init__(self, cgp, group=None, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        groups = cgp.group_set.all()
        if group:
            groups = cgp.group_set.exclude(id=group.id)
        self.fields['country'].queryset = Country.objects.exclude(group__in=groups)

    class Meta:
        model = Group
        fields = ("__all__")
        exclude = ("cgp","has_voted",)

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("__all__")
        exclude = ("slug",)

