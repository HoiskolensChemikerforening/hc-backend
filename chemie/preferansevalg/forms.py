import material as M
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from .models import Position, Election, CandidatePref, CandidateRank


class AddPositionForm(forms.ModelForm):
    layout = M.Layout(
        M.Row(M.Column("Navn på verv"), M.Column("Antall plasser"), M.Column("Is gender important?"), M.Column("The important gender"))
    )

    class Meta:
        model = Position
        fields = ("position_name", "spots", "gender", "important_gender")

#TODO check gender check
class AddCandidateForm(forms.ModelForm): #Legge til gender?
    class Meta:
        model = CandidatePref
        fields = ('user','gender',) 
        widgets = {
            "user": autocomplete.ModelSelect2(url="verv:user-autocomplete")
        }

#TODO sjekk til slutt om tid
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
        model = Election
        fields = ["is_open"]


class EndElectionForm(forms.ModelForm):
    pass

# TODO: hmmm må endres etter models.
def candidatesChoices(election=None):
    try:
        position = election.current_position
        choices = position.candidates.all()
    except:  # AttributeError:
        choices = Position.objects.none()
    return choices

class CandidateRankForm(forms.ModelForm):
    class Meta:
        model = CandidateRank
        fields = ['candidate', 'rank']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dette endrer standard "---------" til "Blank" i dropdown-menyen!
        self.fields['candidate'].empty_label = "Blank"

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

class CastVoteForm(forms.Form): #definer p
    candidates = CustomChoiceField(
        widget=CandidateRankForm, queryset=candidatesChoices()
    )

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop("election")
        super().__init__(*args, **kwargs)
        self.fields["candidates"].queryset = candidatesChoices(self.election)

    def is_valid(self, candidate_list, election): #kan være der?
        valid = super(CastVoteForm, self).is_valid()
        if not valid:
            return False
        if len(candidate_list) > election.current_position.spots:
            return False
        return True

    def is_blank(self, candidate_list): #kan være der?
        if len(candidate_list) == 0:
            return True
        return False