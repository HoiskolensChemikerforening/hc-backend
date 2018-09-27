from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from .forms import AddPositionForm, AddCandidateForm, AddVotesCandidateForm, CastVoteForm
from .models import Election, Position, Candidate


def election_is_open():
    is_open = True
    try:
        election = Election.objects.latest('id')
        if not election.is_open:
            is_open = False
    except ObjectDoesNotExist:
        is_open = False
    return is_open


def voting_is_active():
    active = False
    election = Election.objects.latest('id')
    if election.current_position_is_open:
        active = True
    return active


@login_required
def vote(request):
    try:
        election = Election.objects.latest('id')
        voted = request.user.profile.voted
        context = {'election': election, 'voted': voted}
    except:
        context = {'election': None, 'voted': False}
    return render(request, 'elections/election/index.html', context)


@login_required
def results(request):
    try:
        elections = Election.objects.all()
    except:
        elections = None
    context = {
        'elections': elections,
    }
    return render(request, 'elections/election/resultater.html', context)


@login_required
def voting(request):
    if not election_is_open():
        return redirect('elections:vote')
    else:
        voted = request.user.profile.voted
        election = Election.objects.latest('id')
        if election.current_position_is_open:
            if not voted:
                form = CastVoteForm(request.POST or None, election=election)
                if request.method == 'POST':
                    profile = request.user.profile
                    if form.is_valid():
                        candidates = form.cleaned_data.get('candidates')
                        successful_vote = election.vote(profile, candidates, blank=False)
                    elif 'Stem blankt' in request.POST.getlist('Blank'):
                        successful_vote = election.vote(profile, candidates=None, blank=True)
                    else:
                        context = {
                            'form': form,
                            'position': election.current_position,
                            'candidates': election.current_position.candidates.all(),
                        }
                        return render(request, 'elections/election/vote.html', context)
                    if successful_vote:
                        return redirect('elections:has_voted')
                else:
                    # TODO: Test these lines
                    context = {
                        'form': form,
                        'position':  election.current_position,
                        'candidates': election.current_position.candidates.all(),
                    }
                    return render(request, 'elections/election/vote.html', context)
            return redirect('elections:has_voted')
        return redirect('elections:vote')


@login_required
def has_voted(request):
    if not election_is_open():
        return redirect('elections:vote')
    else:
        election = Election.objects.latest('id')
        if not election.current_position_is_open:
            return redirect('elections:vote')
        # TODO: Test below
        voted = request.user.profile.voted
        if not voted:
            return redirect('elections:vote')
        return render(request, 'elections/election/vote_ended.html')


@permission_required('elections.add_election')
@login_required
def admin_start_election(request): # OK
    if election_is_open():
        election = Election.objects.latest('id')
        if voting_is_active():
            return redirect('elections:admin_start_voting', pk=election.current_position.id)
        return redirect('elections:admin_register_positions')
    if request.method == 'POST': # brukeren trykker på knappen
        Election.objects.create(is_open=True)
        return redirect('elections:admin_register_positions')
    return render(request, 'elections/admin/admin_start_election.html')


@permission_required('elections.add_election')
@login_required
def admin_register_positions(request):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    else:
        form = AddPositionForm(request.POST or None)
        election = Election.objects.latest('id')
        if voting_is_active():
            return redirect('elections:admin_start_voting', pk=election.current_position.id)
        if request.method == "POST":
            if "Delete" in request.POST: # delete posisjon
                position_id = request.POST.get("Delete", "0")
                position = election.positions.get(id=int(position_id))
                election.delete_position(position)
            # Selve formen fr registrering av posisjon
            if form.is_valid():
                # lager en ny posistion objekt som vi legger inn i vår election
                new_position = form.cleaned_data['position_name'] #position field
                # lager en liste som skjekker at vi ikke alt har lagt til vervet i election
                current_positions_in_election = list()
                for i in election.positions.all():
                    current_positions_in_election.append(i.position_name)
                if new_position not in current_positions_in_election: # hvis vi ikke har lagt til vervet allerede
                    spots = form.cleaned_data['spots']  # spots field
                    new_position_object = Position.objects.create(position_name=str(new_position), spots=int(spots))  # lager et position objetkt
                    election.positions.add(new_position_object)
                    election.save()
        positions = election.positions.all()
        context = {
            'form': form,
            'positions': positions
        }
        return render(request, 'elections/admin/admin_positions.html', context)


@permission_required('elections.add_election')
@login_required
def admin_register_candidates(request, pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    else:
        if voting_is_active():
            election = Election.objects.latest('id')
            return redirect('elections:admin_start_voting',pk=election.current_position.id)
        position = get_object_or_404(Position, pk=pk) # henter ut position som skal legge verv til
        add_candidate_form = AddCandidateForm(request.POST or None)
        if request.method == 'POST':
            if 'OK' in request.POST: # Hvis brukeren skal avgi forhåndsstemmer
                form = AddVotesCandidateForm(request.POST)
                if form.is_valid():
                    preVotes = form.cleaned_data['preVotes']
                    candidate_username = request.POST.get("OK", "1")
                    candidate_user_object = User.objects.get(username=candidate_username)
                    all_candidates = position.candidates.all()
                    candidate_object = all_candidates.get(user=candidate_user_object)
                    candidate_object.votes = preVotes
                    candidate_object.save()
            elif 'Delete' in request.POST: # hvis brukeren skal slette candidaten fra posisjonen.
                form = AddVotesCandidateForm(request.POST)
                if form.is_valid():
                    candidate_username = request.POST.get("Delete", "0")
                    candidate_user_object = User.objects.get(username=candidate_username)
                    all_candidates = position.candidates.all()
                    candidate_object = all_candidates.get(user=candidate_user_object)
                    position.candidates.remove(candidate_object)  # sletter brukeren fra stillingen
                    candidate_object.delete()
                    position.save()
            elif 'addCandidate' in request.POST:
                if add_candidate_form.is_valid():
                    user = add_candidate_form.cleaned_data['user']
                    position_candidates = position.candidates.all()
                    to_be_added = False if user in [usr.user for usr in position_candidates] else True
                    if to_be_added:
                        candidate = Candidate.objects.create(user=user)
                        position.candidates.add(candidate)
                        position.save()
            elif 'startVoting' in request.POST:
                election = Election.objects.latest('id')
                if not election.current_position_is_open:
                    election.start_current_election(position)
                return redirect('elections:admin_start_voting', pk=position.id)

        candidates = position.candidates.all()
        context = {
            'candidates': candidates,
            'position': position,
            'add_candidate_form': add_candidate_form
        }
        return render(request, 'elections/admin/admin_candidates.html', context)


@permission_required('elections.add_election')
@login_required
def admin_voting_is_active(request, pk):
    # TODO: Test this entire function
    if not election_is_open():
        return redirect('elections:admin_start_election')
    if not voting_is_active():
        return redirect('elections:admin_register_positions')

    election = Election.objects.latest('id')
    if request.method == 'POST':
        if 'endVoting' in request.POST:
            election.current_position.end_voting_for_position()
            return redirect('elections:admin_results',pk=pk)
    context = {
        'election': election
    }
    return render(request, 'elections/admin/admin_start_voting.html', context)


@permission_required('elections.add_election')
@login_required
def admin_results(request,pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    election = Election.objects.latest('id')
    if voting_is_active():
        return redirect('elections:admin_start_voting', pk=pk)
    position = election.positions.get(id=pk)
    context = {
        'candidates': position.candidates.all(),
        'current_position': position,
        'total_votes': position.total_votes,
        'winners': position.winners.all()
    }
    return render(request, 'elections/admin/admin_results.html', context)


@permission_required('elections.add_election')
@login_required
def admin_end_election(request):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    election = Election.objects.latest('id')
    if voting_is_active():
        return redirect('elections:admin_start_voting', pk=election.current_position.id)
    election.end_election()
    return redirect('elections:results')




"""
     Her er et utkast på å skjekke om en kanditat har vunnet med alminnelig flertall.
    
    ALLMENN_FLERTALL = {
    'pHormand/pHorquinde'
    }
    
    winners = current_election.winners.all()
    candidates = election.current_election.candidates.all()

    if current_election.position_name in ALLMENN_FLERTALL:
        totalVotes = 0
        for candidate in candidates:
            totalVotes += candidate.votes
        foundWinner = False
        lowestVote = 1
        for winner in winners:
            print(winner.votes)
            print(totalVotes)
            margin = float(winner.votes/totalVotes)
            if margin<lowestVote:
                lowestVote=margin
            print(margin)
            if margin >= 0.5:
                election.current_election.winners.clear()
                election.current_election.winners.add(winner)
                election.current_election.save()
                election.save()
                foundWinner = True
        print(foundWinner)
        if not foundWinner:
            #TODO fjerne kandidaten med lavest score fra posisjon
            #election.current_election.candidates.remove(votes=lowestVote)
            election.current_election.save()
            election.save()
            #TODO bytte ut admin_register_positions og heller legge in pk for å sende oss tilbake til admin_start_voting
            return redirect('elections:admin_register_positions')
    """
