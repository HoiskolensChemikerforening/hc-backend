import pytest
from ..models import Candidates, Position
from .factories import CandidateFactory


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

    new_candidates = create_candidates
    candidates = create_candidates
    position = positions[0]
    position.candidates.add(*candidates)
    candidate = candidates[0]
    position.candidates.remove(candidate)
    assert candidate not in list(position.candidates.all())
    position.candidates.add(new_candidates[0])
    assert candidate in list(position.candidates.all())
    position.delete_candidates(candidate)
    assert not candidate


@pytest.mark.django_db
def test_delete_position(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.add_position(positions)

    position = positions[0]
    position.candidates.add(*candidates)
    election.delete_position(positions)

    # Refetch all objects, since they have been deleted, and references are stale
    candidates = Candidates.objects.all()
    positions = election.positions.all()
    assert positions.count() is 0
    assert candidates.count() is 0
