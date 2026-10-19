import material as M
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from .models import PositionPref, ElectionPref, CandidatePref, CandidateRank


class AddPositionForm(forms.ModelForm):
    layout = M.Layout(
        #M.Row(M.Column("Navn på verv"), M.Column("Antall plasser"), M.Column("Is gender important?"), M.Column("The important gender"))
        M.Row(M.Column("Navn på verv"), M.Column("Antall plasser"))
    )

    class Meta:
        model = PositionPref
        #fields = ("position_name", "spots", "gender", "important_gender")
        fields = ("position_name", "spots")

#TODO check gender check
class AddCandidateForm(forms.ModelForm): #Legge til gender?
    class Meta:
        model = CandidatePref
        #fields = ('user','gender',) 
        fields = ('user',)
        widgets = {
            "user": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }

#TODO sjekk til slutt om tid
class AddPrevoteForm(forms.ModelForm):
    class Meta:
        model = PositionPref
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

#TODO sjekk til slutt elns
class AddPreVoteToCandidateForm(forms.ModelForm):
    class Meta:
        model = CandidatePref
        fields = ["pre_votes"]

    def __init__(self, *args, **kwargs):
        super(AddPreVoteToCandidateForm, self).__init__(*args, **kwargs)
        self.fields["pre_votes"].label = self.instance.user.get_full_name()


class OpenElectionForm(forms.ModelForm):
    class Meta:
        model = ElectionPref
        fields = ["is_open"]


class EndElectionForm(forms.ModelForm):
    pass

# TODO: hmmm må endres etter models.
def candidatesChoices(election=None):
    try:
        position = election.current_position
        choices = position.candidates.all()
    except:  # AttributeError:
        choices = PositionPref.objects.none()
    return choices

class CandidateRankForm(forms.ModelForm):
    class Meta:
        model = CandidateRank
        fields = ["candidate", "rank"]
        widgets = {
            "candidate": forms.Select(attrs={"class": "form-select"}),
            "rank": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["candidate"].empty_label = "Blank"

class CustomChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Hent profilbilde
        profile_image = getattr(obj.user.profile, "image_primary", None)

        try:
            thumb = get_thumbnail(profile_image, "200x250", crop="center", quality=85)
            image_url = thumb.url
        except Exception:
            image_url = "/static/images/blank_avatar.png"

        image_html = f"""
            <img src="{image_url}" class='class-image p-1 mt-auto'/>
        """
        name_html = f"<p class='vote-name p-2'>{obj.user.get_full_name()}</p>"

        return mark_safe(image_html + name_html)

from django import forms



class CastVoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop("election")
        super().__init__(*args, **kwargs)

        self.candidates = candidatesChoices(self.election)

        for rank in range(1, self.candidates.count() + 1):
            self.fields[f"candidate_{rank}"] = forms.ModelChoiceField(
                queryset=self.candidates,
                label=f"{rank}. plass",
                empty_label="Velg kandidat",
                required=False,
                widget=forms.Select(
                    attrs={"class": "form-select"}
                ),
            )

    def clean(self):
        cleaned_data = super().clean()

        selected_candidates = []
        found_empty = False

        for field_name in self.fields:
            candidate = cleaned_data.get(field_name)

            if candidate is None:
                found_empty = True
                continue

            if found_empty:
                raise forms.ValidationError(
                    "Du må rangere kandidatene i rekkefølge "
                    "fra førsteplass."
                )

            selected_candidates.append(candidate)

        if len(selected_candidates) != len(set(selected_candidates)):
            raise forms.ValidationError(
                "Du kan ikke velge samme kandidat flere ganger."
            )
        
        """
        # Eventuell begrensning på antall rangeringer
        max_ranks = self.election.current_position.spots

        if len(selected_candidates) > max_ranks:
            raise forms.ValidationError(
                f"Du kan maksimalt rangere {max_ranks} kandidater."
            )
        """
        return cleaned_data

    def selected_candidates(self):
        """Returnerer valgte kandidater i prioritert rekkefølge."""
        if not self.is_bound or not self.is_valid():
            return []

        return [
            self.cleaned_data[field_name]
            for field_name in self.fields
            if self.cleaned_data.get(field_name) is not None
        ]

    def is_blank(self):
        """Returnerer True hvis ingen kandidater er valgt."""
        return len(self.selected_candidates()) == 0