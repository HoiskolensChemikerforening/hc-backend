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
    user = create_user
    client.login(username=user.username, password='defaultpassword')
    request = client.get(reverse('elections:voting'))
    assert request.status_code == 302
    assert request.url == reverse('elections:vote')

    election.is_open = True
    election.save()

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
def test_get_vote_page(client, create_user, create_open_election_with_position_and_candidates):
    election = create_open_election_with_position_and_candidates
    position = election.positions.first()
    election.start_current_election(position)
    election.save()
    election.refresh_from_db()

    user = create_user
    client.login(username=user.username, password='defaultpassword')

    # Check that when user accesses url where he has voted, he is redirected to vote page
    request = client.get(reverse('elections:has_voted'), follow=True)
    assert request.status_code == 200
    assert (reverse('elections:voting'), 302) == request.redirect_chain[0]
    assert election.current_position.position_name in request.content.decode('utf-8')

    # Let user access vote page
    request = client.get(reverse('elections:voting'))
    assert request.status_code is 200
    assert position.position_name in request.content.decode('utf-8')
    assert str(position.spots) in request.content.decode('utf-8')
    for candidate in position.candidates.all():
        assert candidate.user.get_full_name() in request.content.decode('utf-8')


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

    # Check that when user accesses url where he has voted, he receives proper message
    request = client.get(reverse('elections:has_voted'))
    assert 'Du har stemt!' in request.content.decode('utf-8')

    # Check that when user tries to vote again, he is redirected
    request = client.post(
        reverse('elections:voting'),
        {'candidates': candidate.id},
        follow=True
    )
    assert 'Du har stemt!' in request.content.decode('utf-8')

    # Close election and check the results
    position.end_voting_for_position()
    election.end_election()
    request = client.get(reverse('elections:results'))
    assert candidate.user.get_full_name() in request.content.decode('utf-8')


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
    for cand in candidates[number_of_winners + 1:]:
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
    client.post(
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


@pytest.mark.django_db
def test_invalid_vote(client, create_user, create_election_with_positions, create_candidates):
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
    # Trying to vote for all candidates, which are more candidates than position spots
    request = client.post(
        reverse('elections:voting'),
        {'candidates': [cand.id for cand in candidates]}
    )
    assert \
        'Du stemte på {} kandidater, og det skal velges {} kandidater' \
        .format(len(candidates), position.spots) \
        in request.content.decode('utf-8')
