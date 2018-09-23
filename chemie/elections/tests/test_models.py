import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from chemie.customprofile.factories import RandomProfileFactory


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
    with pytest.raises(ObjectDoesNotExist) as e_info:
        candidate.refresh_from_db()


@pytest.mark.django_db
def test_delete_position(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates
    election.add_position(positions)

    position = positions[0]
    position.candidates.add(*candidates)
    election.delete_position(position)
    election.delete_position(positions)

    # Refetch all objects, since they have been deleted, and references are stale
    with pytest.raises(ObjectDoesNotExist) as e_info:
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
    position.end_voting_for_position()
    assert list(position.winners.all()) == list(winner_candidates)


@pytest.mark.django_db
def test_start_current_election(create_election_with_positions, create_candidates):
    election, positions = create_election_with_positions
    candidates = create_candidates

    total_votes = 0
    for i in range(len(candidates)):
        candidates[i].votes = i + 1
        candidates[i].save()
        total_votes += candidates[i].votes

    position = positions[0]
    position.candidates.add(*candidates)

    # Fetch all profiles and fake that they have voted
    profiles = RandomProfileFactory.create_batch(10)
    for profile in profiles:
        profile.voted = True
        profile.save()

    election.start_current_election(position.id)
    assert election.current_position == position

    # Check that users can now vote again
    for profile in profiles:
        profile.refresh_from_db()
        assert profile.voted is False

    assert election.current_position_is_open is True
    assert election.current_position.total_votes is total_votes


@pytest.mark.django_db
def test_end_election(create_election_with_positions):
    election, _ = create_election_with_positions

    election.end_election()
    assert election.is_open is False

    election.is_open = True
    election.save()
    assert election.is_open is True

    election.end_election()
    assert election.is_open is False


@pytest.mark.django_db
def test_start_current_election(create_election_with_positions, create_candidates, create_user):
    election, positions = create_election_with_positions
    candidates = create_candidates
    candidate = candidates[0]

    # Prepare the election
    position = positions[0]
    position.candidates.add(*candidates)
    election.start_current_election(position)

    # Fetch user
    profile = create_user.profile

    # Set an a vote variable
    votes = 0

    # Let user vote blank
    election.vote(profile, candidates=None, blank=True)
    votes += 1
    assert election.current_position.total_votes is votes
    for cand in candidates:
        assert cand.votes is 0

    # Let user vote for single candidate
    profile.voted = False
    profile.save()
    election.vote(profile, candidate, blank=False)
    votes += 1
    assert election.current_position.total_votes is votes
    assert candidate.votes is 1

    # Let user vote for several candidates
    profile.voted = False
    profile.save()
    election.vote(profile, candidates, blank=False)
    votes += len(candidates)
    for cand in candidates:
        cand.refresh_from_db()
        if cand is candidate:
            assert cand.votes is 2
        else:
            assert cand.votes is 1
    assert election.current_position.total_votes is votes
    assert profile.voted is True
