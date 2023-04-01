from django import forms
from .models import Group, Country


class GroupForm(forms.ModelForm):
    """
    Generates a form to create/edit Group objects.
    fields: real_name, country, song_name, audience, group_leaders, group_members
    excluded fields (must be populated in view): cgp, has_voted
    """

    country = forms.ModelChoiceField(queryset=None, label='Land')
    def __init__(self, cgp, group=None, *args, **kwargs):
        """
        Overwrites the init method to prevent used countries from showing up in the countries field.
        Updates the country queryset by excluding all countries related to the passed CGP object.
        Except for the country of the group passed to the init method. This should be the group to be modified or None,
        so that the current country can be chosen when editing.

        Args:
            cgp: current CGP object
            group: current Group object to be edited or None when creating objects
            *args
            **kwargs

        Returns:
            Group form object
        """
        super(GroupForm, self).__init__(*args, **kwargs)
        groups = cgp.group_set.all()
        if group:
            groups = cgp.group_set.exclude(id=group.id)
        self.fields['country'].queryset = Country.objects.exclude(group__in=groups)

    class Meta:
        model = Group
        fields = ("__all__")
        exclude = ("cgp", "has_voted",)

class CountryForm(forms.ModelForm):
    """
    Generates a form to create/edit Country objects.
    fields: country_name, image
    excluded fields (must be populated in view): slug
    """
    class Meta:
        model = Country
        fields = ("__all__")
        exclude = ("slug",)

