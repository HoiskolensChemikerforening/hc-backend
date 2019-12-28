import pytest
from django.shortcuts import reverse

from chemie.elections.models import Ticket


@pytest.mark.django_db
def test_user_not_logged_in(client):
    # Try to access front page
    request = client.get(reverse("elections:index"))
    assert request.status_code == 302
    assert reverse("login") in request.url


@pytest.mark.django_db
def test_election_not_open(client, create_user):
    user = create_user
    client.login(username=user.username, password="defaultpassword")

    request = client.get(reverse("elections:index"))
    assert "Valget har ikke åpnet enda" in request.content.decode("utf-8")
    assert "Resultater fra tidligere valg" in request.content.decode("utf-8")

    request = client.get(reverse("elections:vote"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")

    request = client.get(reverse("elections:has_voted"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")


@pytest.mark.django_db
def test_election_is_open_no_position_open(
    client, create_user, create_election_with_positions
):
    election, positions = create_election_with_positions
    user = create_user
    client.login(username=user.username, password="defaultpassword")
    # Access the vote page. Get redirected to index
    request = client.get(reverse("elections:vote"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")

    election.is_open = True
    election.save()

    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("elections:vote"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")

    request = client.get(reverse("elections:has_voted"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")


@pytest.mark.django_db
def test_open_for_voting_with_and_without_checkin(
    client, create_user, create_open_election_with_position_and_candidates
):
    election = create_open_election_with_position_and_candidates
    position = election.positions.first()
    election.start_current_position_voting(position.id)
    election.save()

    user = create_user
    client.login(username=user.username, password="defaultpassword")

    # User not checked in
    request = client.get(reverse("elections:index"))
    assert request.status_code == 200
    assert "Du har ikke sjekket inn" in request.content.decode("utf-8")

    request = client.get(reverse("elections:vote"))
    assert request.status_code == 302
    assert request.url == reverse("elections:index")

    # User has checked in
    user.profile.eligible_for_voting = True
    user.profile.save()
    request = client.get(reverse("elections:index"))
    assert request.status_code == 200
    assert "Gå til avstemning" in request.content.decode("utf-8")

    request = client.get(reverse("elections:vote"))
    assert request.status_code == 200
    assert "Stem" in request.content.decode("utf-8")


# client.login(username=user.username, password="defaultpassword")
# request = client.get(reverse("elections:vote"))
# assert request.status_code is 200
# assert "Klargjøres til valg" in request.content.decode("utf-8")


@pytest.mark.django_db
def test_get_vote_page(
    client, create_user, create_open_election_with_position_and_candidates
):
    election = create_open_election_with_position_and_candidates
    position = election.positions.first()
    election.start_current_position_voting(position.id)
    election.save()
    election.refresh_from_db()

    user = create_user
    user.profile.eligible_for_voting = True
    user.profile.save()
    client.login(username=user.username, password="defaultpassword")

    # Check that when user accesses url where he has voted, he is redirected to vote page
    request = client.get(reverse("elections:has_voted"), follow=True)
    assert request.status_code == 200
    assert (reverse("elections:vote"), 302) == request.redirect_chain[0]
    assert election.current_position.position_name in request.content.decode(
        "utf-8"
    )

    # Let user access vote page
    request = client.get(reverse("elections:vote"))
    assert request.status_code == 200
    assert position.position_name in request.content.decode("utf-8")
    assert str(position.spots) in request.content.decode("utf-8")
    for candidate in position.candidates.all():
        assert candidate.user.get_full_name() in request.content.decode(
            "utf-8"
        )


@pytest.mark.django_db
def test_vote_for_one_user(
    client, create_user, create_election_with_positions, create_candidates
):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    candidate, position = candidates[0], positions[0]
    position.candidates.add(*candidates)
    election.positions.add(position)
    election.start_current_position_voting(position.id)
    election.save()
    election.refresh_from_db()

    assert election.current_position == position
    election_candidates = election.current_position.candidates.all()
    for cand in candidates:
        assert cand in election_candidates

    user = create_user
    user.profile.eligible_for_voting = True
    user.profile.save()

    # Vote for the candidate chosen
    client.login(username=user.username, password="defaultpassword")
    request = client.post(
        reverse("elections:vote"), {"candidates": candidate.id},
    )
    assert request.url == reverse("elections:has_voted")

    # Check that when user tries to vote again, he is redirected
    request = client.post(
        reverse("elections:vote"), {"candidates": candidate.id}, follow=True
    )
    assert (reverse("elections:has_voted"), 302) == request.redirect_chain[0]
    assert "Din stemme har blitt registrert" in request.content.decode("utf-8")

    # Check that when user accesses url where he has voted, he receives proper message
    request = client.get(reverse("elections:has_voted"))
    assert request.status_code == 200
    assert "Din stemme har blitt registrert" in request.content.decode("utf-8")

    # Check that only one vote ticket was submitted
    assert Ticket.objects.all().count() == 1

    # Close voting and assign votes to candidates by counting tickets
    election.end_current_position_voting()
    position.calculate_candidate_votes()

    # Make sure no blank votes were received
    assert position.get_blank_votes() == position.get_blank_votes()
    candidate.refresh_from_db()
    assert candidate.votes == 1
    assert candidate.pre_votes == 0
    for cand in candidates[1:]:
        cand.refresh_from_db()
        assert cand.votes == 0
        assert cand.pre_votes == 0
    user.profile.refresh_from_db()
    assert user.profile.voted is True


@pytest.mark.django_db
def test_vote_for_multiple_users(
    client, create_user, create_election_with_positions, create_candidates
):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    candidate, position = candidates[0], positions[0]
    position.candidates.add(*candidates)
    election.positions.add(position)
    election.start_current_position_voting(position.id)
    election.save()
    election.refresh_from_db()

    number_of_winners = position.spots
    winner_candidates = []
    for i in range(number_of_winners):
        winner_candidates.append(candidates[i])

    user = create_user
    user.profile.eligible_for_voting = True
    user.profile.save()
    client.login(username=user.username, password="defaultpassword")
    client.post(
        reverse("elections:vote"),
        {"candidates": [cand.id for cand in winner_candidates],},
    )
    # Close voting and assign votes to candidates by counting tickets
    election.end_current_position_voting()
    position.calculate_candidate_votes()

    # Count votes
    assert position.get_blank_votes() == 0
    for cand in winner_candidates:
        cand.refresh_from_db()
        assert cand.votes == 1
        assert cand.pre_votes == 0
    for cand in candidates[number_of_winners + 1 :]:
        cand.refresh_from_db()
        assert cand.votes == 0
    position.refresh_from_db()
    assert position.get_total_votes() == number_of_winners
    user.profile.refresh_from_db()
    assert user.profile.voted is True


@pytest.mark.django_db
def test_vote_blank(
    client, create_user, create_election_with_positions, create_candidates
):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    position = positions[0]
    position.candidates.add(*candidates)
    election.positions.add(position)
    election.start_current_position_voting(position.id)
    election.save()
    election.refresh_from_db()

    user = create_user
    user.profile.eligible_for_voting = True
    user.profile.save()
    client.login(username=user.username, password="defaultpassword")
    client.post(reverse("elections:vote"), {"candidates": []})

    # Close voting and assign votes to candidates by counting tickets
    election.end_current_position_voting()
    position.calculate_candidate_votes()

    # Count votes
    for cand in candidates:
        cand.refresh_from_db()
        assert cand.votes == 0
    position.refresh_from_db()
    assert position.get_total_votes() == 1
    assert position.get_blank_votes() == 1
    user.profile.refresh_from_db()
    assert user.profile.voted is True


@pytest.mark.django_db
def test_invalid_vote(
    client, create_user, create_election_with_positions, create_candidates
):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.is_open = True
    position = positions[0]
    position.candidates.add(*candidates)
    election.positions.add(position)
    election.start_current_position_voting(position.id)
    election.save()
    election.refresh_from_db()

    user = create_user
    user.profile.eligible_for_voting = True
    user.profile.save()
    client.login(username=user.username, password="defaultpassword")
    # Trying to vote for all candidates, which are more candidates than position spots
    request = client.post(
        reverse("elections:vote"),
        {"candidates": [cand.id for cand in candidates]},
    )
    # Submitting a vote containing too many candidates is checked with Javascript
    # The user is therefore redirected
    assert request.status_code == 302
    assert request.url == reverse("elections:has_voted")

    # Close voting and assign votes to candidates by counting tickets
    election.end_current_position_voting()
    position.calculate_candidate_votes()
    assert Ticket.objects.all().count() == 0
    for candidate in candidates:
        candidate.refresh_from_db()
        assert candidate.pre_votes == 0
    assert user.profile.voted is False
