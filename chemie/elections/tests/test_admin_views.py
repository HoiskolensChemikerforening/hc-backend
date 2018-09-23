import pytest
from django.shortcuts import reverse
from ..models import Election, Candidates
from django.core.exceptions import ObjectDoesNotExist

@pytest.mark.django_db
def test_basic_user_admin_page_no_open_election(client, create_user):
    user = create_user

    client.login(username=user.username, password='defaultpassword')

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_start_election'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_end_election'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_register_positions'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_results'))
    assert request.status_code == 302
    assert reverse('login') in request.url


@pytest.mark.django_db
def test_admin_user_admin_page_no_open_election(client, create_admin_user):
    user = create_admin_user
    client.login(username=user.username, password='defaultpassword')

    # Check that admin user can access start election
    request = client.get(reverse('elections:admin_start_election'))
    assert request.status_code == 200
    assert 'Trykk på Start for å sette igang et valg' in request.content.decode('utf-8')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_end_election'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_register_positions'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_results'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')


@pytest.mark.django_db
def test_admin_open_election(client, create_admin_user):
    user = create_admin_user
    client.login(username=user.username, password='defaultpassword')
    assert Election.objects.all().count() == 0
    client.post(reverse('elections:admin_start_election'))
    assert Election.objects.all().count() == 1
    election = Election.objects.all().first()
    assert election.positions.all().count() == 0
    assert election.is_open
    assert not election.current_position_is_open
    assert election.current_position is None


@pytest.mark.django_db
def test_admin_add_positions(client,create_admin_user, create_open_election):
    admin = create_admin_user
    client.login(username=admin.username, password='defaultpassword')
    election = create_open_election
    position_name = "position_name"
    position_spots = 2
    request = client.post(
        reverse('elections:admin_register_positions'),
        {
            'position_name': position_name,
            'spots': position_spots
        })

    assert election.positions.all().count() == 1
    assert election.positions.all().first().position_name == position_name
    assert election.positions.all().first().spots == position_spots
    assert election.positions.all().first().total_votes == 0
    assert election.positions.all().first().candidates.all().count() == 0
    assert not election.positions.all().first().voting_done
    assert election.positions.all().first().winners.all().count() == 0




@pytest.mark.django_db
def test_delete_position(client,create_admin_user, create_election_with_positions):
    admin = create_admin_user
    client.login(username=admin.username, password='defaultpassword')
    election,postitions = create_election_with_positions
    election.is_open = True
    election.add_position(postitions)

    # create_election_with_positions will allways create five positions
    assert election.positions.all().count() == 5

    position = postitions[0]
    assert position in election.positions.all()
    request = client.post(reverse('elections:admin_register_positions'), {'Delete': position.id})
    assert election.positions.all().count() == 4
    with pytest.raises(ObjectDoesNotExist) as e_info:
        position.refresh_from_db()


@pytest.mark.django_db
def test_add_candidates(client,create_admin_user,create_election_with_positions,create_user):
    admin = create_admin_user
    client.login(username=admin.username, password='defaultpassword')
    election, postitions = create_election_with_positions
    election.is_open = True
    position = postitions[0]
    election.add_position(position)
    election.save()
    user = create_user

    request = client.post(
        reverse('elections:admin_register_candidates', kwargs={'pk': position.id}),
        {
            "candidate_user": user.id,
            "addCandidate": "Legg til kandidat"
         }
    )

    position.refresh_from_db()
    assert position.candidates.all().count() == 1
    candidate = Candidates.objects.get(candidate_user=user)
    assert candidate is not None
    assert candidate.votes == 0
    assert not candidate.winner
    assert candidate in position.candidates.all()


@pytest.mark.django_db
def test_add_pre_votes_to_candidate(client,create_admin_user,create_open_election_with_position_and_candidates):
    admin = create_admin_user
    client.login(username=admin.username, password='defaultpassword')
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    number_of_candidates = len(position.candidates.all())
    candidate = position.candidates.all().first()
    pre_votes = 5
    client.post(
        reverse('elections:admin_register_candidates', kwargs={'pk': position.id}),
        {
            "preVotes": pre_votes,
            "OK":candidate.candidate_user.username,
        }
    )
    candidate.refresh_from_db()
    position.refresh_from_db()
    assert candidate.votes == 5
    assert position.total_votes == 5

    # Testing that the votes of other candidates has not changed.
    assert len(position.candidates.filter(votes=0)) == number_of_candidates-1







