from decimal import Decimal

import pytest
from django.shortcuts import reverse

from chemie.shop.models import ShoppingCart, Item


def try_to_buy_item(client, items):
    if type(items) == Item:
        item = items
        client.post(reverse("shop:index"), data={"buy": f"{item.id}-1"})
    elif type(items) == list and type(items[0]) == Item:
        for item in items:
            client.post(reverse("shop:index"), data={"buy": f"{item.id}-1"})
    else:
        s = (
            "Items must either be of type Item or of type "
            "list with entries consisting of Item objects"
        )
        raise TypeError(s)
    request = client.post(reverse("shop:index"), data={"checkout": "checkout"})
    return request


@pytest.mark.django_db
def test_create_cart_without_items_on_visit_shop(client, create_user_no_perms):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:index"))
    assert request.status_code == 200
    cart = ShoppingCart(client)
    assert not cart.cart.keys()


@pytest.mark.django_db
def test_add_items_to_cart(client, create_user_no_perms, create_item):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    cart = ShoppingCart(client)
    # Try to add item to cart
    item = create_item
    request = client.post(reverse("shop:index"), data={"buy": f"{item.id}-1"})
    assert request.status_code == 200
    cart = ShoppingCart(client)
    assert list(cart.cart.keys()) == [f"{item.name}"]


@pytest.mark.django_db
def test_buy_item_and_checkout_no_money(
    client, create_user_no_perms, create_item
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    item = create_item
    # Try to buy item
    request = try_to_buy_item(client, item)
    assert request.status_code == 200
    assert "Du har itj nok HC-coins, kiis" in request.content.decode("utf-8")


@pytest.mark.django_db
def test_buy_item_and_checkout_with_money(
    client, create_user_no_perms, create_item
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    item = create_item
    # Refill balance and buy
    user.profile.balance += item.price
    user.profile.save()
    user.refresh_from_db()
    # Try to buy item
    request = try_to_buy_item(client, item)
    user.refresh_from_db()
    assert request.status_code == 200
    assert "Kontoen din er trukket" in request.content.decode("utf-8")
    assert user.profile.balance == 0


@pytest.mark.django_db
def test_buy_item_and_checkout_with_too_little_money(
    client, create_user_no_perms, create_item
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    item = create_item
    # Refill balance with 10% less than price and try to buy
    balance = item.price * Decimal("0.9")
    user.profile.balance += balance
    user.profile.save()
    user.refresh_from_db()
    # Try to buy item
    request = try_to_buy_item(client, item)
    user.refresh_from_db()
    assert request.status_code == 200
    assert "Du har itj nok HC-coins, kiis" in request.content.decode("utf-8")
    assert user.profile.balance == balance


@pytest.mark.django_db
def test_buy_several_items_and_checkout_with_money(
    client, create_user_no_perms, create_multiple_items
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    items = create_multiple_items
    balance = 0
    for item in items:
        balance += item.price
    user.profile.balance = balance
    user.profile.save()
    user.refresh_from_db()
    request = try_to_buy_item(client, items)
    user.refresh_from_db()
    assert request.status_code == 200
    assert "Kontoen din er trukket" in request.content.decode("utf-8")
    assert user.profile.balance == 0


@pytest.mark.django_db
def test_buy_several_items_and_checkout_without_money(
    client, create_user_no_perms, create_multiple_items
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    items = create_multiple_items
    balance = 0
    for item in items:
        balance += item.price
    balance = balance * Decimal("0.9")
    user.profile.balance = balance
    user.profile.save()
    user.refresh_from_db()
    request = try_to_buy_item(client, items)
    user.refresh_from_db()
    assert request.status_code == 200
    assert "Du har itj nok HC-coins, kiis" in request.content.decode("utf-8")
    assert user.profile.balance == balance
