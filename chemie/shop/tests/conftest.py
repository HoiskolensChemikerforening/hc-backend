from io import BytesIO

import pytest
from PIL import Image
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import InMemoryUploadedFile

from chemie.customprofile.factories import RandomProfileFactory
from chemie.shop.tests.factories import ItemFactory, CategoryFactory
from django.contrib.contenttypes.models import ContentType
from chemie.shop.models import Category


@pytest.fixture(scope="function")
# Base user with profile and all perms
def create_user_base():
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password("defaultpassword")
    new_user.save()
    return new_user


@pytest.fixture(scope="function")
# Base user with profile and all perms
def create_second_user_base():
    new_profile = RandomProfileFactory.create()
    new_user = new_profile.user
    new_user.set_password("defaultpassword")
    new_user.save()
    return new_user


@pytest.fixture(scope="function")
def create_permissions():
    # Category test is tied to the category model since there are multiple cateory models in other apps
    content_model = ContentType.objects.get_for_model(Category)
    p_item = Permission.objects.get_or_create(name="Can add item")[0]
    p_category = Permission.objects.get_or_create(
        name="Can add category", content_type=content_model
    )[0]
    p_refill = Permission.objects.get_or_create(name="Can refill balance")[0]
    return p_item, p_category, p_refill


# Fixture for client with user profile and all perms
@pytest.fixture(scope="function")
def create_user_all_perms(create_user_base, create_permissions):
    p_item, p_category, p_refill = create_permissions
    user = create_user_base
    user.user_permissions.add(p_item)
    user.user_permissions.add(p_category)
    user.user_permissions.add(p_refill)
    user.save()
    return user


# Fixture for client with user profile and item perms
@pytest.fixture(scope="function")
def create_user_item_perms(create_user_base, create_permissions):
    p_item, p_category, p_refill = create_permissions
    user = create_user_base
    user.user_permissions.add(p_item)
    user.save()
    return user


# Fixture for client with user profile and category perms
@pytest.fixture(scope="function")
def create_user_category_perms(create_user_base, create_permissions):
    p_item, p_category, p_refill = create_permissions
    user = create_user_base
    user.user_permissions.add(p_category)
    user.save()
    return user


# Fixture for client with user profile and refill perms
@pytest.fixture(scope="function")
def create_user_refill_perms(create_user_base, create_permissions):
    p_item, p_category, p_refill = create_permissions
    user = create_user_base
    user.user_permissions.add(p_refill)
    user.save()
    return user


# Fixture for client with user profile and no perms
@pytest.fixture(scope="function")
def create_user_no_perms(create_user_base):
    user = create_user_base
    return user


@pytest.fixture(scope="function")
def create_category():
    return CategoryFactory.create()


@pytest.fixture(scope="function")
def create_item():
    return ItemFactory.create()


@pytest.fixture(scope="function")
def create_multiple_items():
    return ItemFactory.create_batch(3)


@pytest.fixture(scope="function")
def create_image():
    im = Image.new(mode="RGB", size=(200, 200))  # create a new image using PIL
    im_io = BytesIO()  # a BytesIO object for saving image
    im.save(im_io, "JPEG")  # save the image to im_io
    im_io.seek(0)  # seek to the beginning

    image = InMemoryUploadedFile(
        im_io,
        None,
        "random-name.jpg",
        "image/jpeg",
        len(im_io.getvalue()),
        None,
    )
    return image
