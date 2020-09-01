import pytest
from django.shortcuts import reverse

from chemie.shop.models import Order, RefillReceipt
from chemie.shop.tests.test_payments import try_to_buy_item


@pytest.mark.django_db
def test_order_is_created_when_one_item_bought(
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
    try_to_buy_item(client, item)
    order = Order.objects.latest("id")
    order_items = order.items.all()
    order_item = order_items[0]
    # How many items are in the order
    assert order_items.count() == 1
    # What is on the order
    assert order_item.item == item
    # How many items of that 1 item was bought
    assert order_item.quantity == 1
    # Who made the order?
    assert order.buyer == user
    # What was the total price on the order?
    assert order.get_total_price() == item.price


@pytest.mark.django_db
def test_order_is_created_when_several_items_bought(
    client, create_user_no_perms, create_multiple_items
):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    items = create_multiple_items
    # Refill balance and buy
    balance = 0
    for item in items:
        balance += item.price
    user.profile.balance = balance
    user.profile.save()
    user.refresh_from_db()
    # Try to buy item
    try_to_buy_item(client, items)
    order = Order.objects.latest("id")
    order_items = order.items.all()
    # How many items on the order?
    assert order_items.count() == len(items)
    # Check that 1 of each item was bought
    for item in order_items:
        assert item.quantity == 1


@pytest.mark.django_db
def test_refill_equates_to_spent_plus_balance(
    client, create_user_refill_perms, create_multiple_items
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    items = create_multiple_items
    # Refill balance and buy
    amount = 10
    for item in items:
        amount += item.price
    client.post(
        reverse("shop:refill"), data={"receiver": user.id, "amount": amount}
    )
    user.refresh_from_db()
    # Try to buy item
    try_to_buy_item(client, items)
    # Get the order
    order = Order.objects.latest("id")
    spent_money = order.get_total_price()
    # Get the refill receipt
    receipt = RefillReceipt.objects.latest("id")
    assert receipt.amount == spent_money + user.profile.balance


@pytest.mark.django_db
def test_refill_amount_receiver_and_provider_ok(
    client, create_user_refill_perms
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    client.get(reverse("shop:index"))
    amount = 10
    client.post(
        reverse("shop:refill"), data={"receiver": user.id, "amount": amount}
    )
    user.refresh_from_db()
    receipt = RefillReceipt.objects.latest("id")
    assert receipt.provider == user
    assert receipt.receiver == user
    assert receipt.amount == amount
