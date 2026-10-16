from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CastVoteForm
from .models import ElectionPref, PositionPref


@login_required
def index(request):
    eligible = request.user.profile.eligible_for_voting
    try:
        election = ElectionPref.get_latest_election()
        voted = request.user.profile.voted
        context = {"election": election, "voted": voted, "eligible": eligible}
    except ObjectDoesNotExist:
        context = {"election": None, "voted": False, "eligible": eligible}

    return render(request, "elections/election/index.html", context)


@login_required
def vote(request): #TODO den og dens side må endres? Skal ha sliders og sånt
    if not ElectionPref.current_position_is_active():
        return redirect("preferansevalg:index")

    if not request.user.profile.eligible_for_voting:
        return redirect("preferansevalg:index")

    if request.user.profile.voted:
        return redirect("preferansevalg:index")

    election = ElectionPref.get_latest_election()
    form = CastVoteForm(request.POST or None, election=election)

    if request.method == "POST":
        user = request.user
        candidate_list = request.POST.getlist("candidates")

        if form.is_valid(candidate_list, election):
            election.current_position.vote(candidate_list, user)

        elif form.is_blank(candidate_list):
            election.current_position.vote_blank(user)

        return redirect("preferansevalg:has_voted_pref")

    cands = election.current_position.candidates.all().order_by("id")
    context = {
        "form": form,
        "position": election.current_position,
        "candidates": cands,
    }

    return render(request, "elections/election/vote_pref.html", context)


@login_required
def has_voted(request):
    if not ElectionPref.current_position_is_active():
        return redirect("preferansevalg:index")

    if not request.user.profile.eligible_for_voting:
        return redirect("preferansevalg:index")

    if not request.user.profile.voted:
        return redirect("preferansevalg:vote_pref")

    return render(request, "elections/election/vote_ended_pref.html")


@login_required
def view_previous_elections_index(request):
    try:
        election = ElectionPref.get_latest_election()
        if election.is_open:
            return redirect("preferansevalg:admin_register_positions_pref")
    except ObjectDoesNotExist:
        return redirect("preferansevalg:index")

    elections = ElectionPref.objects.filter(
        date__range=["2019-04-29", "2200-01-01"]
    ).order_by(
        "-date"
    )  # Reason for filtering after 29.04.2019 is because of changes to the old system
    context = {"elections": elections}
    return render(
        request, "elections/election/previous_election_index_pref.html", context
    )


@login_required
def view_previous_election(request, pk):
    election = get_object_or_404(ElectionPref, pk=pk)
    if election.is_open:
        return redirect("preferansevalg:admin_register_positions_pref")
    else:
        positions = election.positions.all()
        n_voters = [
            position.get_number_of_voters()
            for position in election.positions.all()
        ]

        total_votes = [
            position.get_total_votes() for position in election.positions.all()
        ]

        blank_votes = [
            position.get_blank_votes() for position in election.positions.all()
        ]

        context = {
            "election": election,
            "positions": positions,
            "voter_list": n_voters,
            "total_votes": total_votes,
            "blank_votes": blank_votes,
        }

        return render(
            request, "elections/election/previous_election_pref.html", context
        )