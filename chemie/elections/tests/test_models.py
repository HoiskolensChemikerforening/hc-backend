import pytest
from django.core.exceptions import ObjectDoesNotExist

@pytest.mark.django_db
def test_inital_election(create_election_with_positions):
    election, positions = create_election_with_positions
    assert not election.is_open
    assert not election.current_position_is_open
    assert not election.current_position
    assert len(election.positions.all()) is 0


@pytest.mark.django_db
def test_add_positions_to_election(create_election_with_positions):
    election, positions = create_election_with_positions
    election.positions.add(*positions)
    assert len(election.positions.all()) is not 0
    assert not election.current_position
    assert not election.is_open
    election.current_position = positions[0]
    assert election.current_position is not None
    for position in positions:
        assert position.candidates.all().count() is 0
        assert position.winners.all().count() is 0
        assert position.total_votes is 0
        assert position.voting_done is False


@pytest.mark.django_db
def test_add_candidate(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    election.add_position(positions)
    for position in positions:
        candidates = create_candidates
        position.candidates.add(*candidates)
        assert len(position.candidates.all()) is len(candidates)
        assert position.winners.all().count() is 0
        assert position.total_votes is 0
        for candidate in position.candidates.all():
            assert candidate.votes is 0
            assert candidate.winner is False
            assert candidate.candidate_user is not None


@pytest.mark.django_db
def test_delete_single_candidate(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    election.add_position(positions)

    candidates = create_candidates
    position = positions[0]
    position.candidates.add(*candidates)
    candidate = candidates[0]
    position.candidates.remove(candidate)
    assert candidate not in list(position.candidates.all())
    position.candidates.add(candidate)
    assert candidate in list(position.candidates.all())
    position.delete_candidates(candidate)
    with pytest.raises(ObjectDoesNotExist):
        candidate.refresh_from_db()


@pytest.mark.django_db
def test_delete_position(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.add_position(positions)

    position = positions[0]
    position.candidates.add(*candidates)
    election.delete_position(positions)

    # Refetch all objects, since they have been deleted, and references are stale
    with pytest.raises(ObjectDoesNotExist):
        for position in positions:
            position.refresh_from_db()
        for candidate in candidates:
            candidate.refresh_from_db()

@pytest.mark.django_db
def test_get_current_position_winners(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates

    position = positions[0]
    number_of_winners = position.spots
    winner_candidates = []
    for i in range(number_of_winners):
        candidates[i].votes = i + 1
        candidates[i].save()
        winner_candidates.append(candidates[i])

    position.candidates.add(*candidates)
    position.get_current_position_winners()
    assert list(position.winners.all()) == list(winner_candidates)







