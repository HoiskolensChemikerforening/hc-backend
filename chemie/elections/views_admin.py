from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, reverse

from chemie.customprofile.forms import GetRFIDForm, ManualRFIDForm
from chemie.customprofile.models import ProfileManager, Profile
from .forms import AddPositionForm, AddCandidateForm
from .forms import AddPrevoteForm, AddPreVoteToCandidateForm
from .models import Election, Position, Candidate


@permission_required("elections.add_election")
@login_required
def admin_start_election(request):
    if Election.latest_election_is_open():
        election = Election.get_latest_election()

        if election.current_position_is_active():
            return redirect(
                "elections:admin_voting_active",
                pk=election.current_position.id,
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
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:

        election = Election.get_latest_election()
        form = AddPositionForm(request.POST or None)

        if request.method == "POST":
            # Selve formen for registrering av posisjon

            if form.is_valid():
                new_position = form.cleaned_data["position_name"]
                spots = form.cleaned_data["spots"]
                election.add_position(new_position, spots)

        done_positions = election.positions.filter(is_done=True).order_by(
            "position_name"
        )
        not_done_positions = election.positions.filter(is_done=False).order_by(
            "position_name"
        )
        checkin_count = Profile.objects.filter(
            eligible_for_voting=True
        ).count()
        context = {
            "form": form,
            "done_positions": done_positions,
            "not_done_positions": not_done_positions,
            "checkin_count": checkin_count,
        }

        return render(request, "elections/admin/admin_positions.html", context)


@permission_required("elections.add_election")
@login_required
def admin_delete_position(request):
    if request.method == "POST":
        position_id = request.POST.get("Delete", "0")
        election = Election.get_latest_election()
        election.delete_position(position_id)
    return redirect("elections:admin_register_positions")


@permission_required("elections.add_election")
@login_required
def admin_register_candidates(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected
    else:

        position = get_object_or_404(Position, pk=pk)
        add_candidate_form = AddCandidateForm(request.POST or None)
        if request.method == "POST":

            if add_candidate_form.is_valid():
                user = add_candidate_form.cleaned_data["user"]
                position.add_candidate(user)

        candidates = position.candidates.all().order_by("user")
        context = {
            "candidates": candidates,
            "position": position,
            "add_candidate_form": add_candidate_form,
        }

        return render(
            request, "elections/admin/admin_candidates.html", context
        )


@permission_required("elections.add_election")
@login_required
def admin_delete_candidate(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:

        if request.method == "POST":
            candidate_username = request.POST.get("Delete", "0")
            position = Position.objects.get(id=pk)
            position.delete_candidate(candidate_username)
            if position.candidates.count() == 0:
                position.number_of_prevote_tickets = 0
                position.save()
            elif position.number_of_prevote_tickets != 0:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Pass på at totalt antall forhåndsstemmer er korrekt før du starter valget!",
                    extra_tags="Obs!",
                )
    return redirect("elections:admin_register_candidates", pk=pk)


@permission_required("elections.add_election")
@login_required
def admin_start_voting(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:

        if request.method == "POST":
            election = Election.get_latest_election()
            election.start_current_position_voting(pk)

        return redirect("elections:admin_register_candidates", pk=pk)


@permission_required("elections.add_election")
@login_required
def admin_acclamation(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:

        if request.method == "POST":
            election = Election.get_latest_election()
            election.start_current_position_voting(pk)
            election.end_current_position_voting_by_acclamation()
        return redirect("elections:admin_register_positions")


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

                if prevote_form.prevotes_allowed(
                    formset, position
                ):  # checks that the ammount of pre_votes does not exceed feasable amount
                    prevote_form.save()

                    for form in formset:
                        form.save()

                    return redirect(
                        reverse(
                            "elections:admin_register_candidates",
                            kwargs={"pk": position.id},
                        )
                    )
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "For mange stemmer på kandidatene enn det som er mulig med antall personer som har forhåndstemt",
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
        election.end_current_position_voting()
        return redirect("elections:admin_results", pk=pk)

    total_voters = election.current_position.get_number_of_voters()
    context = {"election": election, "total_voters": total_voters}
    return render(request, "elections/admin/admin_voting_active.html", context)


@permission_required("elections.add_election")
@login_required
def admin_results(request, pk):
    is_redirected, redir_function = Election.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected

    election = Election.get_latest_election()
    if not election.current_position.id == pk:
        election.change_current_position(pk)

    position = election.current_position

    position.calculate_candidate_votes()
    blank_votes = position.get_blank_votes()
    number_of_voters = position.get_number_of_voters()
    total_votes = position.get_total_votes()
    number_of_tickets = position.get_number_of_tickets()
    context = {
        "position": position,
        "candidates": position.candidates.all(),
        "number_of_voters": number_of_voters,
        "total_votes": total_votes,
        "blank_votes": blank_votes,
        "number_of_tickets": number_of_tickets,
    }
    return render(request, "elections/admin/admin_results.html", context)


@permission_required("elections.add_election")
@login_required
def admin_end_election(request):
    if Election.objects.all().count() <= 0:
        return redirect("elections:admin_start_election")

    election = Election.get_latest_election()
    if election.is_open:
        election.end_election()

    return redirect("elections:admin_start_election")


@permission_required("elections.add_election")
def open_election_for_everyone(request):
    for profile in Profile.objects.all():
        profile.eligible_for_voting = True
        profile.save()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Alle brukere har nå mulighet til å stemme.",
        extra_tags="Vellykket!",
    )

    return redirect("elections:admin_register_positions")


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
                    extra_tags="Advarsel",
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
                    extra_tags="Innsjekk",
                )

            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "{} har sjekket ut".format(profile.user.get_full_name()),
                    extra_tags="Utsjekk",
                )

        return redirect("elections:checkin")
    else:
        is_open = Election.latest_election_is_open()
        context = {"form": form, "is_open": is_open}

    return render(request, "elections/check_in.html", context)


@permission_required("elections.add_election")
@login_required
def manual_rfid_status(request):
    form = ManualRFIDForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data.get("user")
            try:
                profile = Profile.objects.get(user=user)
                profile.eligible_for_voting = not profile.eligible_for_voting
                profile.save()
                status = profile.eligible_for_voting

                if status:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "{} har sjekket inn".format(
                            profile.user.get_full_name()
                        ),
                        extra_tags="Innsjekk",
                    )

                else:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "{} har sjekket ut".format(
                            profile.user.get_full_name()
                        ),
                        extra_tags="Utsjekk",
                    )
            except:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Brukeren finnes ikke.",
                    extra_tags="Advarsel",
                )
        return redirect("elections:checkin_manually")
    else:
        is_open = Election.latest_election_is_open()
        context = {"form": form, "is_open": is_open}

    return render(request, "elections/check_in_manually.html", context)
