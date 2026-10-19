import pytest
from django.core.exceptions import ObjectDoesNotExist
import factory
from chemie.customprofile.models import Profile


@pytest.mark.django_db
def test_initial_election(create_election_with_positions):
    election, positions = create_election_with_positions
    assert not election.is_open
    assert election.positions.count() == 0
    assert not election.current_position
    for profile in Profile.objects.all():
        assert profile.eligible_for_voting is False
        assert profile.voted is False


@pytest.mark.django_db
def test_add_positions_to_election(create_election_with_positions):
    election, _ = create_election_with_positions
    spots = [1, 2, 3]
    for i in range(len(spots)):
        position_name = factory.Faker("first_name")
        election.add_position(position_name, spots[i])
        assert election.positions.latest("id").spots == spots[i]

    assert not election.current_position
    assert not election.is_open
    assert election.current_position is None
    for position in election.positions.all():
        assert position.candidates.all().count() == 0
        assert position.tickets.all().count() == 0
        assert position.number_of_prevote_tickets == 0
        assert position.is_active is False
        assert position.is_done is False
    assert election.positions.count() == len(spots)


@pytest.mark.django_db
def test_add_candidate(create_election_with_positions, create_user):
    election, positions = create_election_with_positions
    election.positions.add(*positions)
    for position in positions:
        user = create_user
        position.add_candidate(user)
        assert len(position.candidates.all()) == 1
        for candidate in position.candidates.all():
            assert candidate.votes == 0
            assert candidate.user is not None


@pytest.mark.django_db
def test_delete_single_candidate(
    create_election_with_positions, create_candidates
):
    election, positions = create_election_with_positions
    election.positions.add(*positions)

    candidates = create_candidates
    position = positions[0]
    position.candidates.add(*candidates)
    candidate = candidates[0]
    position.candidates.remove(candidate)
    assert candidate not in list(position.candidates.all())
    position.candidates.add(candidate)
    assert candidate in list(position.candidates.all())
    position.delete_candidate(candidate.user.username)
    with pytest.raises(ObjectDoesNotExist) as _:
        candidate.refresh_from_db()
    assert candidate not in list(position.candidates.all())


@pytest.mark.django_db
def test_delete_position(
    create_election_with_positions, create_candidates, create_user
):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.positions.add(*positions)
    n_positions = election.positions.count()
    election.positions.first().candidates.add(*candidates)
    for position in election.positions.all():
        election.delete_position(position.id)
        assert election.positions.count() == n_positions - 1
        n_positions -= 1
    assert n_positions == 0

    with pytest.raises(ObjectDoesNotExist) as _:
        for position in positions:
            position.refresh_from_db()
        for candidate in candidates:
            candidate.refresh_from_db()
    assert election.positions.count() == 0


@pytest.mark.django_db
def test_voting_outcome(
    create_open_election_with_position_and_candidates, create_user
):
    election = create_open_election_with_position_and_candidates
    position = election.positions.first()
    assert position.number_of_prevote_tickets == 0
    assert position.get_number_of_voters() == 0
    assert position.get_non_blank_votes() == 0
    assert position.get_blank_votes() == 0

    user = create_user
    election.start_current_position_voting(position.id)

    position.calculate_candidate_votes()
    for candidate in position.candidates.all():
        assert candidate.pre_votes == 0
        assert candidate.votes == 0

    position.vote_blank(user)
    assert user.profile.voted is True
    assert position.number_of_prevote_tickets == 0
    assert position.get_number_of_voters() == 1
    assert position.get_non_blank_votes() == 0
    assert position.get_blank_votes() == 1

    position.calculate_candidate_votes() == 0
    for candidate in position.candidates.all():
        assert candidate.pre_votes == 0
        assert candidate.votes == 0

    user.profile.voted = False
    vote_candidates = position.candidates.all()[0:2]

    position.vote(vote_candidates, user)
    assert user.profile.voted is True
    assert position.number_of_prevote_tickets == 0
    assert position.get_number_of_voters() == 2
    assert position.get_non_blank_votes() == 1
    assert position.get_blank_votes() == 1

    position.calculate_candidate_votes() == 0
    for candidate in position.candidates.all():
        assert candidate.pre_votes == 0

        if candidate.id == vote_candidates[0].id:
            assert candidate.votes == 1
        elif candidate.id == vote_candidates[1].id:
            assert candidate.votes == 1
        else:
            assert candidate.votes == 0
    election.end_current_position_voting()
    assert not election.current_position.is_active
    assert election.current_position.is_done
