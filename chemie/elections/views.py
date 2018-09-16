from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Election, Position, Candidates
from .forms import AddPositionForm, AddCandidateForm, OpenElectionForm, AddVotesCandidateForm, CastVoteForm
from django.shortcuts import redirect


def check_latest_election():
    check = True
    try:
        election = Election.objects.latest('id')
        if not election.is_open:
            check = False
    except AttributeError:
        check = False
    return check


@login_required
def vote(request):
    try:
        election = Election.objects.latest('id')
        voted = request.user.profile.voted
        context = {'election': election, 'voted':voted}
    except:
        context = {'election':None, 'voted':False}
    return render(request, 'elections/election/index.html', context)

@login_required
def resultater(request):
    try:
        elections = Election.objects.all()
    except:
        elections = None
    context = {
        'elections':elections,
    }
    return render(request,'elections/election/resultater.html',context)

@login_required
def voting(request):
    if not check_latest_election():
        return redirect('elections:vote')
    else:
        voted = request.user.profile.voted
        election = Election.objects.latest('id')
        if election.current_position_is_open:
            if not voted:
                form = CastVoteForm(request.POST or None, election=election)
                if request.method == 'POST':
                    if election.vote(request,form):
                        return redirect('elections:has_voted')
                else:
                    context= {
                        'form': form,
                        'position':  election.current_position,
                        'candidates':election.current_position.candidates.all(),
                        'picture':election.current_position.candidates.latest('id').candidate_user.profile.image_primary
                    }
                    print(election.current_position.candidates.latest('id').candidate_user.profile.image_primary)
                    return render(request, 'elections/election/vote.html', context)
            return redirect('elections:has_voted')
        return redirect('elections:vote')


@login_required
def has_voted(request):
    if not check_latest_election():
        return redirect('elections:vote')
    else:
        election = Election.objects.latest('id')
        if not election.current_position_is_open:
            return redirect('elections:vote')
        voted = request.user.profile.voted
        if not voted:
            return redirect('elections:vote')
        return render(request, 'elections/election/vote_ended.html')


@permission_required('valg.add_Election')
@login_required
def admin_start_election(request): # OK
    if request.method == 'POST': # brukeren trykker på knappen
        Election.objects.create(is_open=True)
        election = Election.objects.latest('id')
        election.save()
        return redirect('elections:admin_register_positions')
    else:
        try: # kjører try fordi det kan hende det ikke finnes et election object
            election = Election.objects.latest('id')
            if election.is_open: # hvis det alt finnes en election skal vi bare hoppe til hovedsiden
                return redirect('elections:admin_register_positions')
        except:
            pass
    return render(request, 'elections/admin/admin_start_election.html')

@permission_required('valg.add_Election')
@login_required
def admin_register_positions(request):
    if not check_latest_election():
        return redirect('elections:admin_start_election')
    else:
        election = Election.objects.latest('id')
        if request.method == "POST":
            if "Delete" in request.POST: # delete posisjon
                position_name = request.POST.get("Delete", "0")
                election_position = election.positions.filter(position_name=position_name)
                #todo change filter to get
                election_position[0].delete_position(election=election)
            # Selve formen fr registrering av posisjon
            form = AddPositionForm(request.POST)
            if form.is_valid():
                # lager en ny posistion objekt som vi legger inn i vår election
                new_position = form.cleaned_data['position_name'] #position field
                # lager en liste som skjekker at vi ikke alt har lagt til vervet i election
                current_positions_in_election = list()
                for i in election.positions.all():
                    current_positions_in_election.append(i.position_name)
                if not new_position in current_positions_in_election: # hvis vi ikke har lagt til vervet allerede
                    spots = form.cleaned_data['spots']  # spots field
                    new_position_object = Position.objects.create(position_name=str(new_position), spots=int(spots))  # lager et position objetkt
                    election.positions.add(new_position_object)
                    election.save()
        form = AddPositionForm()
        positions = election.positions.all()
        context = {
            'form': form,
            'positions': positions
        }
        return render(request, 'elections/admin/admin_positions.html', context)


@permission_required('valg.add_Election')
@login_required
def admin_register_candidates(request, pk):
    if not check_latest_election():
        return redirect('elections:admin_start_election')
    else:
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
                    candidate_object = all_candidates.get(candidate_user=candidate_user_object)
                    candidate_object.votes = preVotes
                    candidate_object.save()
            elif 'Delete' in request.POST: # hvis brukeren skal slette candidaten fra posisjonen.
                form = AddVotesCandidateForm(request.POST)
                if form.is_valid():
                    candidate_username = request.POST.get("Delete", "0")
                    candidate_user_object = User.objects.get(username=candidate_username)
                    all_candidates = position.candidates.all()
                    candidate_object = all_candidates.get(candidate_user=candidate_user_object)
                    position.candidates.remove(candidate_object)  # sletter brukeren fra stillingen
                    candidate_object.delete()
                    position.save()
            elif 'addCandidate' in request.POST:
                if add_candidate_form.is_valid():
                    user = add_candidate_form.cleaned_data['candidate_user']
                    position_candidates = position.candidates.all()
                    to_be_added = False if user in [usr.candidate_user for usr in position_candidates] else True
                    if to_be_added:
                        candidate = Candidates.objects.create(candidate_user=user)
                        position.candidates.add(candidate)
                        position.save()

        candidates = position.candidates.all()
        form = AddCandidateForm() # overskriver form her for at sist lagt til bruker ikke står som default for neste innlegging
        context = {
            'candidates': candidates,
            'form': form,
            'position': position,
            'add_candidate_form': add_candidate_form
        }
        return render(request, 'elections/admin/admin_candidates.html', context)


@permission_required('valg.add_Election')
@login_required
def admin_start_voting(request, pk):
    if not check_latest_election():
        return redirect('elections:admin_start_election')
    else:
        election = Election.objects.latest('id')
        if not election.current_position_is_open:
            election.start_current_election(pk)
        context = {
            'election': election
        }
        return render(request, 'elections/admin/admin_start_voting.html', context)



@permission_required('valg.add_Election')
@login_required
def admin_results(request):
    if not check_latest_election():
        return redirect('elections:admin_start_election')
    else:
        election = Election.objects.latest('id')
        election.current_position.get_current_position_winners()
        election.current_position_is_open = False
        election.current_position.voting_done = True
        election.current_position.save()
        election.save()

        context = {
            'candidates': election.current_position.candidates.all(),
            'current_position': election.current_position,
            'total_votes': election.current_position.total_votes,
            'winners':election.current_position.winners.all()
            }

        return render(request, 'elections/admin/admin_results.html', context)
@permission_required('valg.add_Election')
@login_required
def admin_end_election(request):
    if not check_latest_election():
        return redirect('elections:admin_start_election')
    else:
        election = Election.objects.latest('id')
        election.end_election()
        return redirect('elections:resultater')




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
