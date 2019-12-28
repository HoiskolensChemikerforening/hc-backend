from decimal import Decimal

import pytest
from django.shortcuts import reverse
from chemie.customprofile.models import Profile
from chemie.shop.models import Item, Category, HappyHour


@pytest.mark.django_db
def test_create_category(client, create_user_category_perms):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.post(
        reverse("shop:add-category"), data={"name": "Kategori"}
    )
    assert request.status_code == 200
    assert "Kategori" in request.content.decode("utf-8")
    assert Category.objects.get(name="Kategori") is not None


@pytest.mark.django_db
def test_create_item(
    client, create_user_item_perms, create_category, create_image
):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    image = create_image
    cat = create_category
    request = client.post(
        reverse("shop:add-item"),
        data={
            "name": "Vare",
            "price": Decimal(10),
            "category": cat.id,
            "image": image,
        },
    )
    # Name is unique, so we can find the item by name
    assert request.status_code == 200
    assert "Vare" in request.content.decode("utf-8")
    assert Item.objects.get(name="Vare") is not None


@pytest.mark.django_db
def test_refill_balance(client, create_user_refill_perms):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    receiver = user
    amount = Decimal(100)
    request = client.post(
        reverse("shop:refill"),
        data={"receiver": receiver.id, "amount": amount},
    )
    user.profile.refresh_from_db()
    assert request.status_code == 200
    assert user.profile.balance == amount
    # We have not touched any other balances
    all_profiles = Profile.objects.all()
    other_profiles = all_profiles.exclude(user=user)
    for p in other_profiles:
        assert p.balance == 0
