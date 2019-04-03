import material as M
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import Position, Election, Candidate, Ticket


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


#     class Meta:
#         model = Election
#         fields = ["current_position_is_open"]


def candidatesChoices(election=None):
    try:
        position = election.current_position
        choices = position.candidates.all()
    except:  # AttributeError:
        choices = Position.objects.none()
    return choices


class CustomChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = mark_safe(
            "<p class='vote-name'>%s %s </p>"
            % (obj.user.first_name, obj.user.last_name)
        )
        try:
            image = mark_safe(
                "<img src='%s' class='vote-image' style='max-width:6rem; border-radius:0.5rem'/>"
                % obj.user.profile.image_primary.url
            )
        except:
            image = mark_safe(
                "<img src='%s' class='vote-image' style='max-width:6rem; border-radius:0.5rem'/>"
                % "/static/images/blank_avatar.png"
            )
        return image + name


class CastVoteForm(forms.Form):
    candidates = CustomChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=candidatesChoices()
    )

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop("election")
        super().__init__(*args, **kwargs)
        self.fields["candidates"].queryset = candidatesChoices(self.election)

    def is_valid(self, request, election):
        valid = super(CastVoteForm, self).is_valid()
        if not valid:
            return False
        candidate_list = request.POST.getlist("candidates")
        if len(candidate_list) > election.current_position.spots:
            return False
        return True

    def is_blank(self, request, election):
        candidate_list = request.POST.getlist("candidates")
        if len(candidate_list) == 0:
            return True
        return False

    def clean_candidates(self):
        candidates = self.cleaned_data["candidates"].all()
        count = candidates.count()
        if count > self.election.current_position.spots or count <= 0:
            raise ValidationError(
                "Stem på litt færre folk da kis. "
                "Du stemte på {} kandidater, "
                "og det skal velges {} kandidater til vervet.".format(
                    count, self.election.current_position.spots
                )
            )
        else:
            return candidates
