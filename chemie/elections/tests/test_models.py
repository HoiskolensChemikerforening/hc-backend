import pytest
from chemie.events.tests.conftest import create_admin_user, create_user

@pytest.mark.django_db
def test_inital_election(create_election_with_positions):
    pass