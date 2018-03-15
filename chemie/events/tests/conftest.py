from chemie.customprofile.factories import RandomProfileFactory
import pytest

# Fixture for logged in client with user profile
@pytest.fixture(scope='function')
def client_profile(client, superuser=False):
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password('defaultpassword')

    if superuser:
        new_user.is_superuser = True
        new_user.is_staff = True

    new_user.save()
    client.login(username=new_user.username, password='defaultpassword')
    return client


@pytest.fixture(scope='function')
def admin_client(client):
    return client_profile(client, superuser=True)
