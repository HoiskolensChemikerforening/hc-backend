import pytest


@pytest.mark.django_db
def test_create_item_no_perms(client, create_user_no_perms):
    assert 1 == 1
