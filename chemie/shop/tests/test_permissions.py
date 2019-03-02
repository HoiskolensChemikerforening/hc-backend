from decimal import Decimal

import pytest
from django.shortcuts import reverse
from chemie.customprofile.models import Profile

MAX_AMOUNT = 10**4


#################################
############# VIEWS #############
#################################

########### Category ############
@pytest.mark.django_db
def test_create_category_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 200
    request = client.post(
        reverse("shop:add-category"),
        data={
            "name": "Kategori",
        }
    )
    assert request.status_code == 302


@pytest.mark.django_db
def test_create_category_item_perms(client, create_user_item_perms):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_create_category_category_perms(client, create_user_category_perms):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 200
    request = client.post(
        reverse("shop:add-category"),
        data={
            "name": "Kategori",
        }
    )
    assert request.status_code == 302


@pytest.mark.django_db
def test_create_category_refill_perms(client, create_user_refill_perms):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_create_category_no_perms(client, create_user_no_perms):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 302
    assert "/login" in request.url


############# Items #############
@pytest.mark.django_db
def test_create_item_with_item_perms(client, create_user_all_perms, create_category, create_image):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 200
    image = create_image
    cat = create_category
    request = client.post(
        reverse("shop:add-item"),
        follow=True,
        data={
            "name": "Vare",
            "price": Decimal(10),
            "description": "Beskrivelse",
            "category": cat.id,
            "image": image
        }
    )
    assert (reverse("shop:index"), 302) == request.redirect_chain[0]
    assert "Vare" in request.content.decode("utf-8")


@pytest.mark.django_db
def test_create_item_with_item_perms(client, create_user_item_perms, create_category, create_image):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 200
    image = create_image
    cat = create_category
    request = client.post(
        reverse("shop:add-item"),
        follow=True,
        data={
            "name": "Vare",
            "price": Decimal(10),
            "description": "Beskrivelse",
            "category": cat.id,
            "image": image
        }
    )
    assert (reverse("shop:index"), 302) == request.redirect_chain[0]
    assert "Vare" in request.content.decode("utf-8")


@pytest.mark.django_db
def test_create_item_with_category_perms(client, create_user_category_perms):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_create_item_with_refill_perms(client, create_user_refill_perms):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_create_item_no_perms(client, create_user_no_perms):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 302
    assert "/login" in request.url


########### Refill ############
@pytest.mark.django_db
def test_refill_balance_with_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200
    receiver = user
    amount = Decimal(100)
    request = client.post(
        reverse("shop:refill"),
        data={
            "receiver": receiver.id,
            "amount": amount
        }
    )
    user.profile.refresh_from_db()
    assert request.status_code == 200
    assert user.profile.balance == amount
    # We have not touched any other balances
    all_profiles = Profile.objects.all()
    other_profiles = all_profiles.exclude(user=user)
    for p in other_profiles:
        assert p.balance == 0


@pytest.mark.django_db
def test_refill_balance_with_item_perms(client, create_user_item_perms):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_refill_balance_with_category_perms(client, create_user_category_perms):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_refill_balance_with_refill_perms(client, create_user_refill_perms):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200
    receiver = user
    amount = Decimal(100)
    request = client.post(
        reverse("shop:refill"),
        data={
            "receiver": receiver.id,
            "amount": amount
        }
    )
    user.profile.refresh_from_db()
    assert request.status_code == 200
    assert user.profile.balance == amount
    # We have not touched any other balances
    all_profiles = Profile.objects.all()
    other_profiles = all_profiles.exclude(user=user)
    for p in other_profiles:
        assert p.balance == 0


@pytest.mark.django_db
def test_refill_balance_no_perms(client, create_user_no_perms):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url
