import chemie.custommaterial as M
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from .models import Position, Election, Candidate


class AddPositionForm(forms.ModelForm):
    layout = M.Layout(
        M.Row(M.Column("Navn på verv"), M.Column("Antall plasser"))
    )

    class Meta:
        model = Position
        fields = ("position_name", "spots")


class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ("user",)
        widgets = {
            "user": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }


class AddPrevoteForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["number_of_prevote_tickets"]

    def prevotes_allowed(self, formset, position):
        """
        Check that there is not more pre_votes that is feasable for current postion
        with respect to how many peoples that have been prevoted
        """

        n_prevoters = self.cleaned_data["number_of_prevote_tickets"]
        total_prevoters = 0
        for form in formset:
            total_prevoters += form.cleaned_data["pre_votes"]
        if total_prevoters / position.spots > n_prevoters:
            return False
        return True


class AddPreVoteToCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["pre_votes"]

    def __init__(self, *args, **kwargs):
        super(AddPreVoteToCandidateForm, self).__init__(*args, **kwargs)
        self.fields["pre_votes"].label = self.instance.user.get_full_name()


class OpenElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ["is_open"]


class EndElectionForm(forms.ModelForm):
    pass


def candidatesChoices(election=None):
    try:
        position = election.current_position
        choices = position.candidates.all()
    except:  # AttributeError:
        choices = Position.objects.none()
    return choices

'''
class CustomChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = mark_safe(
            f"<p class='vote-name p-2'>{obj.user.first_name} {obj.user.last_name} </p>"
        )

        image = mark_safe(
            f"<img src='{obj.image_url}' class='class-image p-2 mt-auto'/>"
        )

        return image + name
'''
class CustomChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Hent profilbilde
        profile_image = getattr(obj.user.profile, "image_primary", None)

        try:
            thumb = get_thumbnail(profile_image, "400x500", crop="center", quality=85)
            image_url = thumb.url
        except Exception:
            image_url = "/static/images/blank_avatar.png"

        image_html = f"""
            <img src="{image_url}" class='class-image p-1 mt-auto'/>
        """
        name_html = f"<p class='vote-name p-2'>{obj.user.get_full_name()}</p>"

        return mark_safe(image_html + name_html)

class CastVoteForm(forms.Form):
    candidates = CustomChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=candidatesChoices()
    )

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop("election")
        super().__init__(*args, **kwargs)
        self.fields["candidates"].queryset = candidatesChoices(self.election)

    def is_valid(self, candidate_list, election):
        valid = super(CastVoteForm, self).is_valid()
        if not valid:
            return False
        if len(candidate_list) > election.current_position.spots:
            return False
        return True

    def is_blank(self, candidate_list):
        if len(candidate_list) == 0:
            return True
        return False
