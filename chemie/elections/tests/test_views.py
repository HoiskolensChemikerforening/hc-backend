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
def test_vote_for_one_user(client, create_user, create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    candidate, position = candidates[0], positions[0]
    position.candidates.add(*candidates)
    election.add_position(position)
    election.start_current_election(position)
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
        {'candidates': candidate.id}
    )
    assert request.url == reverse('elections:has_voted')
    candidate.refresh_from_db()
    assert candidate.votes == 1
    for cand in candidates[1:]:
        cand.refresh_from_db()
        assert cand.votes == 0
    user.profile.refresh_from_db()
    assert user.profile.voted is True


@pytest.mark.django_db
def test_vote_for_multiple_users(client, create_user, create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    candidate, position = candidates[0], positions[0]
    position.candidates.add(*candidates)
    election.add_position(position)
    election.start_current_election(position)
    election.save()
    election.refresh_from_db()

    number_of_winners = position.spots
    winner_candidates = []
    for i in range(number_of_winners):
        winner_candidates.append(candidates[i])

    user = create_user
    client.login(username=user.username, password='defaultpassword')
    client.post(
        reverse('elections:voting'),
        {'candidates': [cand.id for cand in winner_candidates]}
    )
    for cand in winner_candidates:
        cand.refresh_from_db()
        assert cand.votes is 1
    for cand in candidates[number_of_winners+1:]:
        cand.refresh_from_db()
        assert cand.votes is 0
    position.refresh_from_db()
    assert position.total_votes is number_of_winners
    user.profile.refresh_from_db()
    assert user.profile.voted is True


@pytest.mark.django_db
def test_vote_blank(client, create_user, create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    position = positions[0]
    position.candidates.add(*candidates)
    election.add_position(position)
    election.start_current_election(position)
    election.save()
    election.refresh_from_db()

    user = create_user
    client.login(username=user.username, password='defaultpassword')
    request = client.post(
        reverse('elections:voting'),
        {'Blank': 'Stem blankt'}
    )
    for cand in candidates:
        cand.refresh_from_db()
        assert cand.votes is 0
    position.refresh_from_db()
    assert position.total_votes is 1
    user.profile.refresh_from_db()
    assert user.profile.voted is True


# @pytest.mark.django_db
# def test_invalid_vote(client, create_user, create_election_with_positions, create_candidates):
#     election, positions = create_election_with_positions
#     candidates = create_candidates
#     election.is_open = True
#     position = positions[0]
#     position.candidates.add(*candidates)
#     election.add_position(position)
#     election.start_current_election(position)
#     election.save()
#     election.refresh_from_db()
#
#     user = create_user
#     client.login(username=user.username, password='defaultpassword')
#     # Trying to vote for all candidates, which are more candidates than position spots
#     request = client.post(
#         reverse('elections:voting'),
#         {'candidates': [cand.id for cand in candidates]}
#     )
#     """
#     client.post(
#         reverse('elections:voting'),
#         {'candidates': [cand.id for cand in winner_candidates]}
#     )
#     """
#     assert 'Gjør det rett a kis' in request.content.decode('utf-8')
