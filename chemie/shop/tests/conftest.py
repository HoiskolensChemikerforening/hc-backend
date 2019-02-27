import pytest

from django.contrib.auth.models import Permission
from chemie.customprofile.factories import RandomProfileFactory


# Fixture for client with user profile and all perms
@pytest.fixture(scope="function")
def create_user_all_perms(perms=[1, 1, 1]):
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password("defaultpassword")
    p_item = Permission.objects.create(name="shop.add_item")
    p_category = Permission.objects.create(name="shop.add_category")
    p_refill = Permission.objects.get_or_create(
        name="customprofile.refill_balance"
    )
    if perms[0]:
        new_user.user_permissions.add(p_item)
    if perms[1]:
        new_user.user_permissions.add(p_category)
    if perms[2]:
        new_user.user_permissions.add(p_refill)
    new_user.save()
    return new_user


# Fixture for client with user profile and item perms
@pytest.fixture(scope="function")
def create_user_item_perms():
    return create_user_all_perms([1, 0, 0])


# Fixture for client with user profile and category perms
@pytest.fixture(scope="function")
def create_user_category_perms():
    return create_user_all_perms([0, 1, 0])


# Fixture for client with user profile and refill perms
@pytest.fixture(scope="function")
def create_user_refill_perms():
    return create_user_all_perms([0, 0, 1])


# Fixture for client with user profile and no perms
@pytest.fixture(scope="function")
def create_user_no_perms():
    return create_user_all_perms([0, 0, 0])
