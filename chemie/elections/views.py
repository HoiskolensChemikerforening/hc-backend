from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import CastVoteForm
from .models import Election


@login_required
def index(request):
    eligible = request.user.profile.eligible_for_voting
    try:
        election = Election.get_latest_election()
        voted = request.user.profile.voted
        context = {"election": election, "voted": voted, "eligible": eligible}
    except ObjectDoesNotExist:
        context = {"election": None, "voted": False, "eligible": eligible}

    return render(request, "elections/election/index.html", context)


@login_required
def vote(request):
    if not Election.current_position_is_active():
        return redirect("elections:index")

    if not request.user.profile.eligible_for_voting:
        return redirect("elections:index")

    if request.user.profile.voted:
        return redirect("elections:has_voted")

    election = Election.get_latest_election()
    form = CastVoteForm(request.POST or None, election=election)

    if request.method == "POST":
        user = request.user
        candidate_list = request.POST.getlist("candidates")

        if form.is_valid(candidate_list, election):
            election.current_position.vote(candidate_list, user)

        elif form.is_blank(candidate_list):
            election.current_position.vote_blank(user)

        return redirect("elections:has_voted")

    cands = election.current_position.candidates.all().order_by("id")
    context = {
        "form": form,
        "position": election.current_position,
        "candidates": cands,
    }

    return render(request, "elections/election/vote.html", context)


@login_required
def has_voted(request):
    if not Election.current_position_is_active():
        return redirect("elections:index")

    if not request.user.profile.eligible_for_voting:
        return redirect("elections:index")

    if not request.user.profile.voted:
        return redirect("elections:vote")

    return render(request, "elections/election/vote_ended.html")

