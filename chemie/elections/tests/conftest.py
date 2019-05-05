import pytest

from chemie.customprofile.factories import RandomProfileFactory
from chemie.elections.models import Election
from .factories import PositionFactory
from ..models import Candidate


# Fixture for logged in client with user profile
@pytest.fixture(scope="function")
def create_user(superuser=False):
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password("defaultpassword")
    new_user.save()
    return new_user


@pytest.fixture(scope="function")
def create_admin_user():
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password("defaultpassword")
    new_user.is_superuser = True
    new_user.is_staff = True
    new_user.save()
    return new_user


@pytest.fixture(scope="function")
def create_election_with_positions():
    new_election = Election.objects.create()
    positions = PositionFactory.create_batch(5)
    return new_election, positions


@pytest.fixture(scope="function")
def create_open_election_with_position_and_candidates():
    new_election = Election.objects.create()
    new_election.is_open = True
    position = PositionFactory.create()
    number_of_candidates = 4
    profiles = RandomProfileFactory.create_batch(number_of_candidates)
    candidates = []
    for i in range(number_of_candidates):
        profile = profiles[i]
        candidate = Candidate.objects.create(user=profile.user)
        candidates.append(candidate)
    position.candidates.add(*candidates)
    position.save()
    new_election.positions.add(position)
    new_election.save()
    return new_election


@pytest.fixture(scope="function")
def create_open_election():
    new_election = Election.objects.create()
    new_election.is_open = True
    new_election.save()
    return new_election


@pytest.fixture(scope="function")
def create_candidates():
    number_of_candidates = 4
    profiles = RandomProfileFactory.create_batch(number_of_candidates)
    candidates = []
    for i in range(number_of_candidates):
        profile = profiles[i]
        candidate = Candidate.objects.create(user=profile.user)
        candidates.append(candidate)
    return candidates
