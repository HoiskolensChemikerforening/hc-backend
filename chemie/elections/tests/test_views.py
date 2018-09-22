import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_user_not_logged_in(client):
    request = client.get(reverse('elections:vote'))
    assert request.status_code == 302
    assert reverse('login') in request.url


@pytest.mark.django_db
def test_election_not_open(client, create_user):
    user = create_user
    client.login(username=user.username, password='defaultpassword')

    request = client.get(reverse('elections:vote'))
    assert 'Valget har ikke åpnet enda' in request.content.decode('utf-8')
    assert '<a class="button" href="/elections/results">' in request.content.decode('utf-8')

    request = client.get(reverse('elections:has_voted'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url
    request = client.get(reverse('elections:voting'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url


@pytest.mark.django_db
def test_election_is_open(client, create_user, create_election_with_positions):
    election, positions = create_election_with_positions
    election.is_open = True
    election.save()
    user = create_user

    client.login(username=user.username, password='defaultpassword')
    request = client.get(reverse('elections:vote'))
    assert request.status_code is 200
    assert "Klargjøres til valg" in request.content.decode('utf-8')

    request = client.get(reverse('elections:has_voted'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url
    request = client.get(reverse('elections:voting'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url


@pytest.mark.django_db
def test_election_is_open(client, create_user, create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    candidate, position = candidates[0], positions[0]
    position.candidates.add(*candidates)
    election.add_position(position)
    election.start_current_election(position.id)
    election.save()
    election.refresh_from_db()

    assert election.current_position == position
    election_candidates = election.current_position.candidates.all()
    for cand in candidates:
        assert cand in election_candidates

    user = create_user

    client.login(username=user.username, password='defaultpassword')
    request = client.post(
        reverse('elections:voting'),
        {'candidates': [str(candidate.id)]}
    )
    candidate.refresh_from_db()
    assert candidate.votes == 1
    for cand in candidates[1:]:
        cand.refresh_from_db()
        assert cand.votes == 0
