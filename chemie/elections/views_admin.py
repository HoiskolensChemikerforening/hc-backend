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


@permission_required("elections.add_election")
@login_required
def admin_start_election(request):
    if Election.latest_election_is_open():
        election = Election.get_latest_election()
        if election.is_voting_active():
            return redirect(
                "elections:admin_start_voting", pk=election.current_position.id
            )
        return redirect("elections:admin_register_positions")
    if request.method == "POST":  # brukeren trykker på knappen
        Election.create_new_election()
        return redirect("elections:admin_register_positions")
    return render(request, "elections/admin/admin_start_election.html")


@permission_required("elections.add_election")
@login_required
def admin_register_positions(request):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected
    else:
        election = Election.get_latest_election()
        form = AddPositionForm(request.POST or None)
        if request.method == "POST":
            if "Delete" in request.POST:  # delete posisjon
                election.delete_position(request)
                form = AddPositionForm(None)
            # Selve formen fr registrering av posisjon
            if form.is_valid():
                election.add_position(form)

        done_positions = election.positions.filter(is_done=True).order_by(
            "position_name"
        )
        not_done_positions = election.positions.filter(is_done=False).order_by(
            "position_name"
        )
        context = {
            "form": form,
            "done_positions": done_positions,
            "not_done_positions": not_done_positions,
        }
        return render(request, "elections/admin/admin_positions.html", context)


@permission_required("elections.add_election")
@login_required
def admin_register_candidates(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected
    else:
        election = Election.get_latest_election()
        position = get_object_or_404(Position, pk=pk)
        add_candidate_form = AddCandidateForm(request.POST or None)
        if request.method == "POST":
            if "Delete" in request.POST:
                position.delete_candidates(request)
            elif "addCandidate" in request.POST:
                if add_candidate_form.is_valid():
                    position.add_candidates(add_candidate_form)
            elif "startVoting" in request.POST:
                if(election.start_current_position_voting(position)):
                    return redirect("elections:admin_start_voting", pk=position.id)
        candidates = position.candidates.all().order_by("user")
        context = {
            "candidates": candidates,
            "position": position,
            "add_candidate_form": add_candidate_form,
        }
        return render(request, "elections/admin/admin_candidates.html", context)


@permission_required("elections.add_election")
@login_required
def admin_register_prevotes(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected
    else:
        position = get_object_or_404(Position, pk=pk)
        prevote_form = AddPrevoteForm(
            request.POST or None, instance=position, prefix="total_voters"
        )

        # Form for adjusting individual candidate's votes
        CandidateFormSet = modelformset_factory(
            Candidate, form=AddPreVoteToCandidateForm, extra=0
        )
        formset = CandidateFormSet(
            request.POST or None,
            queryset=position.candidates.all().order_by("user"),
            prefix="candidate_forms",
        )
        if request.method == "POST":
            if formset.is_valid() and prevote_form.is_valid():
                prevote_form.save()
                for form in formset:
                    form.save()
                return redirect(
                    reverse(
                        "elections:admin_register_candidates",
                        kwargs={"pk": position.id},
                    )
                )
        context = {
            "prevote_form": prevote_form,
            "candidate_formset": formset,
            "position": position,
        }
        return render(
            request, "elections/admin/admin_add_prevotes.html", context
        )


@permission_required("elections.add_election")
@login_required
def admin_voting_is_active(request, pk):
    if not Election.latest_election_is_open():
        return redirect("elections:admin_start_election")
    election = Election.get_latest_election()
    if request.method == "POST":
        if "endVoting" in request.POST:
            election.current_position.end_voting_for_position()
            return redirect("elections:admin_results", pk=pk)
    total_voters = election.current_position.get_number_of_voters()
    context = {"election": election, "total_voters": total_voters}
    return render(request, "elections/admin/admin_start_voting.html", context)


@permission_required("elections.add_election")
@login_required
def admin_results(request, pk):
    if not election_is_open():
        return redirect("elections:admin_start_election")
    election = Election.objects.latest("id")
    if voting_is_active():
        return redirect("elections:admin_start_voting", pk=pk)
    position = election.positions.get(id=pk)
    total_votes = position.get_total_votes()
    winners = position.winners.all()
    blank_votes = position.blank_votes
    number_of_voters = position.number_of_voters
    if number_of_voters < VOTES_REQUIRED_FOR_VALID_ELECTION:
        messages.add_message(
            request,
            messages.ERROR,
            "OBS!",
            extra_tags="Det ble kun avgitt {} stemmesedler.".format(
                number_of_voters
            ),
        )
    print(blank_votes)
    context = {
        "candidates": position.candidates.all(),
        "total_votes": total_votes,
        "winners": winners,
        "number_of_voters": number_of_voters,
        "blank_votes": blank_votes,
    }
    return render(request, "elections/admin/admin_results.html", context)


@permission_required("elections.add_election")
@login_required
def admin_end_election(request):
    if not election_is_open():
        return redirect("elections:admin_start_election")
    election = Election.objects.latest("id")
    if voting_is_active():
        return redirect(
            "elections:admin_start_voting", pk=election.current_position.id
        )
    election.end_election()
    return redirect("elections:results")


@permission_required("elections.add_election")
@login_required
def change_rfid_status(request):
    form = GetRFIDForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            rfid = form.cleaned_data.get("rfid")
            em_code = ProfileManager.rfid_to_em(rfid)
            try:
                profile = Profile.objects.get(access_card=em_code)
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Studentkortnummeret er ikke registrert enda.",
                )
                return redirect(
                    f"{reverse('profile:add_rfid')}?cardnr={rfid}&redirect={request.get_full_path()}"
                )
            profile.eligible_for_voting = not profile.eligible_for_voting
            profile.save()
            status = profile.eligible_for_voting
            if status:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "{} har sjekket inn".format(profile.user.get_full_name()),
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} har sjekket ut".format(profile.user.get_full_name()),
                )
        return redirect("elections:checkin")
    else:
        is_open = election_is_open()
        context = {"form": form, "is_open": is_open}
    return render(request, "elections/check_in.html", context)

