from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, reverse

from chemie.customprofile.forms import GetRFIDForm, ManualRFIDForm
from chemie.customprofile.models import ProfileManager, Profile
from .forms import AddPositionForm, AddCandidateForm
from .forms import AddPrevoteForm, AddPreVoteToCandidateForm
from .models import ElectionPref, PositionPref, CandidatePref


@permission_required("elections.add_election")
@login_required
def admin_start_election(request):
    if ElectionPref.latest_election_is_open():
        election = ElectionPref.get_latest_election()

        if election.current_position_is_active():
            return redirect(
                "preferansevalg:admin_voting_active_pref",
                pk=election.current_position.id,
            )
        return redirect("preferansevalg:admin_register_positions_pref")

    if request.method == "POST":  # brukeren trykker på knappen
        ElectionPref.create_new_election()
        return redirect("preferansevalg:admin_register_positions_pref")

    return render(request, "elections/admin/admin_start_election_pref.html")


@permission_required("elections.add_election")
@login_required
def admin_register_positions(request):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:
        election = ElectionPref.get_latest_election()
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

        return render(request, "elections/admin/admin_positions_pref.html", context)


@permission_required("elections.add_election")
@login_required
def admin_delete_position(request):
    if request.method == "POST":
        position_id = request.POST.get("Delete", "0")
        election = ElectionPref.get_latest_election()
        election.delete_position(position_id)
    return redirect("preferansevalg:admin_register_positions_pref")


@permission_required("elections.add_election")
@login_required
def admin_register_candidates(request, pk):
    print("Prøver å registrere bruker")
    is_redirected, redir_function = ElectionPref.is_redirected()

    if is_redirected:
        print("is_redirected")
        return redir_function

    position = get_object_or_404(PositionPref, pk=pk)
    print("Position:", position)
    print("Prøver å registrere bruker")

    if request.method == "POST" and "addCandidate" in request.POST:
        form = AddCandidateForm(request.POST)

        print("POST-data:", request.POST)
        print("Er skjemaet gyldig?", form.is_valid())
        print("Skjemafeil:", form.errors.as_data())
        print("Skjemafeil (lesbart):", form.errors)
        print("POST user:", request.POST.get("user"))
        #print("POST gender:", request.POST.get("gender"))

        if form.is_valid():
            user = form.cleaned_data["user"]
            #gender = form.cleaned_data["gender"]

            candidate = position.add_candidate(
                user=user,
            #    gender=gender,
            )

            if candidate is not None:
                return redirect(request.path)

            form.add_error(
                "user",
                "Brukeren er allerede kandidat til denne posisjonen.",
            )
    else:
        form = AddCandidateForm()

    candidates = position.candidates.all().order_by("user")

    context = {
        "candidates": candidates,
        "position": position,
        "add_candidate_form": form,
    }

    return render(
        request,
        "elections/admin/admin_candidates_pref.html",
        context,
    )



@permission_required("elections.add_election")
@login_required
def admin_delete_candidate(request, pk):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:
        if request.method == "POST":
            candidate_username = request.POST.get("Delete", "0")
            position = PositionPref.objects.get(id=pk)
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
    return redirect("preferansevalg:admin_register_candidates_pref", pk=pk)


@permission_required("elections.add_election")
@login_required
def admin_start_voting(request, pk):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:
        if request.method == "POST":
            election = ElectionPref.get_latest_election()
            election.start_current_position_voting(pk)

        return redirect("preferansevalg:admin_register_candidates_pref", pk=pk)


@permission_required("elections.add_election")
@login_required
def admin_acclamation(request, pk):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:  # either voting is active, or election is not open
        return redir_function  # Redirect function from Election.is_redirected
    else:
        if request.method == "POST":
            election = ElectionPref.get_latest_election()
            election.start_current_position_voting(pk)
            election.end_current_position_voting_by_acclamation()
        return redirect("preferansevalg:admin_register_positions_pref")


@permission_required("elections.add_election")
@login_required
def admin_register_prevotes(request, pk):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected
    else:
        position = get_object_or_404(PositionPref, pk=pk)
        prevote_form = AddPrevoteForm(
            request.POST or None, instance=position, prefix="total_voters"
        )

        # Form for adjusting individual candidate's votes
        CandidateFormSet = modelformset_factory(
            CandidatePref, form=AddPreVoteToCandidateForm, extra=0
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
                            "preferansevalg:admin_register_candidates_pref",
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
            request, "elections/admin/admin_add_prevotes_pref.html", context
        )


@permission_required("elections.add_election")
@login_required
def admin_voting_is_active(request, pk):
    if not ElectionPref.latest_election_is_open():
        return redirect("preferansevalg:admin_start_election_pref")

    election = ElectionPref.get_latest_election()
    if request.method == "POST":
        election.end_current_position_voting()
        return redirect("preferansevalg:admin_results_pref", pk=pk)

    total_voters = election.current_position.get_number_of_voters()
    checkin_count = Profile.objects.filter(eligible_for_voting=True).count()
    context = {
        "election": election,
        "total_voters": total_voters,
        "checkin_count": checkin_count,
    }
    return render(request, "elections/admin/admin_voting_active_pref.html", context)


@permission_required("elections.add_election")
@login_required
def admin_results(request, pk):
    is_redirected, redir_function = ElectionPref.is_redirected()
    if is_redirected:
        return redir_function  # Redirect function from Election.is_redirected

    election = ElectionPref.get_latest_election()
    if not election.current_position.id == pk:
        election.change_current_position(pk)

    position = election.current_position

    position.calculate_candidate_votes()
    blank_votes = position.get_blank_votes()
    number_of_voters = position.get_number_of_voters()
    total_votes = position.get_total_votes()  # with blank votes
    number_of_tickets = position.get_number_of_tickets()
    checkin_count = Profile.objects.filter(eligible_for_voting=True).count()
    total_voters = election.current_position.get_number_of_voters()
    #first_time_tickets = position.alle_tickets #queryset?
    
    original_tickets = position.read_orginal_tickets() #liste
    candidate_results = [
        {
            "candidate": kandidat,
            "votes_by_rank": kandidat.get_votes_by_rank_for_Candidate(position),
        }
        for kandidat in position.candidates.all()
    ]
    print("KANDIDATER:", list(position.candidates.all()))

    context = {
        "position": position,
        "candidates": position.candidates.all(),
        "number_of_voters": number_of_voters,
        "total_votes": total_votes,
        "blank_votes": blank_votes,
        "number_of_tickets": number_of_tickets,
        "checkin_count": checkin_count,
        "total_voters": total_voters,
        "candidate_results": candidate_results,
        "original_tickets":original_tickets,
    }
    return render(request, "elections/admin/admin_results_pref.html", context)


@permission_required("elections.add_election")
@login_required
def admin_end_election(request):
    if ElectionPref.objects.all().count() <= 0:
        return redirect("preferansevalg:admin_start_election_pref")

    election = ElectionPref.get_latest_election()
    if election.is_open:
        election.end_election()

    return redirect("preferansevalg:admin_start_election_pref")


@permission_required("elections.add_election")
def open_election_for_everyone(request): #alt med stemmerett kan hentes fra election
    for profile in Profile.objects.all():
        profile.eligible_for_voting = True
        profile.save()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Alle brukere har nå mulighet til å stemme.",
        extra_tags="Vellykket!",
    )

    return redirect("preferansevalg:admin_register_positions_pref")


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

        return redirect("preferansevalg:checkin_pref")
    else:
        is_open = ElectionPref.latest_election_is_open()
        context = {"form": form, "is_open": is_open}

    return render(request, "elections/check_in_pref.html", context)


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
        return redirect("preferansevalg:checkin_manually_pref")
    else:
        is_open = ElectionPref.latest_election_is_open()
        context = {"form": form, "is_open": is_open}

    return render(request, "elections/check_in_manually_pref.html", context)
