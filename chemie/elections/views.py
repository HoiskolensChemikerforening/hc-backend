from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, reverse

from chemie.customprofile.forms import GetRFIDForm
from chemie.customprofile.models import ProfileManager, User, Profile
from .forms import AddPositionForm, AddCandidateForm, CastVoteForm
from .forms import AddPrevoteForm, AddPreVoteToCandidateForm
from .models import Election, Position, Candidate
from .models import VOTES_REQUIRED_FOR_VALID_ELECTION


def election_is_open():
    is_open = True
    try:
        election = Election.objects.latest("id")
        if not election.is_open:
            is_open = False
    except ObjectDoesNotExist:
        is_open = False
    return is_open


def voting_is_active():
    active = False
    election = Election.objects.latest("id")
    if election.current_position_is_open:
        active = True
    return active




@login_required
def vote(request):
    eligible = request.user.profile.eligible_for_voting
    try:
        election = Election.objects.latest("id")
        voted = request.user.profile.voted
        context = {"election": election, "voted": voted, "eligible": eligible}
    except:
        context = {"election": None, "voted": False, "eligible": eligible}
    return render(request, "elections/election/index.html", context)


@login_required
def results(request):
    try:
        elections = Election.objects.all()
    except:
        elections = None
    context = {"elections": elections}
    return render(request, "elections/election/resultater.html", context)


@login_required
def voting(request):
    if not election_is_open():
        return redirect("elections:vote")
    else:
        voted = request.user.profile.voted
        eligible = request.user.profile.eligible_for_voting
        election = Election.objects.latest("id")
        if election.current_position_is_open:
            if eligible and not voted:
                form = CastVoteForm(request.POST or None, election=election)
                if request.method == "POST":
                    profile = request.user.profile
                    candidate_list = request.POST.getlist("candidates")
                    if len(candidate_list) == 0:
                        successful_vote = election.vote(
                            profile, candidates=None, blank=True
                        )
                    elif len(candidate_list) <= election.current_position.spots:
                        if form.is_valid():
                            candidates = form.cleaned_data.get("candidates")
                            successful_vote = election.vote(
                                profile, candidates, blank=False
                            )
                        else:
                            # Un-checks all candidates, since form is invalid
                            form.fields["candidates"].widget.checked_attribute[
                                "checked"
                            ] = False
                            cands = election.current_position.candidates.all()
                            context = {
                                "form": form,
                                "position": election.current_position,
                                "candidates": cands,
                            }
                            return render(
                                request, "elections/election/vote.html", context
                            )
                    else:
                        cands = election.current_position.candidates.all()
                        context = {
                            "form": form,
                            "position": election.current_position,
                            "candidates": cands,
                        }
                        return render(
                            request, "elections/election/vote.html", context
                        )
                    if successful_vote:
                        return redirect("elections:has_voted")
                else:
                    cands = election.current_position.candidates.all().order_by(
                        "id"
                    )
                    context = {
                        "form": form,
                        "position": election.current_position,
                        "candidates": cands,
                    }
                    return render(
                        request, "elections/election/vote.html", context
                    )
        return redirect("elections:vote")


@login_required
def has_voted(request):
    if not election_is_open():
        return redirect("elections:vote")
    else:
        election = Election.objects.latest("id")
        if not election.current_position_is_open:
            return redirect("elections:vote")
        voted = request.user.profile.voted
        if not voted:
            return redirect("elections:voting")
        return render(request, "elections/election/vote_ended.html")

