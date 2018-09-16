import pytest

from chemie.customprofile.factories import RandomProfileFactory


# Fixture for logged in client with user profile
@pytest.fixture(scope='function')
def create_user(superuser=False):
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password('defaultpassword')
    if superuser:
        new_user.is_superuser = True
        new_user.is_staff = True
    new_user.save()
    return new_user


@pytest.fixture(scope='function')
def create_admin_user():
    return create_user(superuser=True)
