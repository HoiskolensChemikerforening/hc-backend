import pytest
from django.shortcuts import reverse
from chemie.shop.urls import urlpatterns

MAX_AMOUNT = 10 ** 4


# --------------------------------- #
# ------------- VIEWS ------------- #
# --------------------------------- #


# ----------- Category ----------- #
@pytest.mark.django_db
def test_view_create_page_category_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_create_page_category_item_perms(client, create_user_item_perms):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_create_page_category_category_perms(
    client, create_user_category_perms
):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_create_page_category_refill_perms(
    client, create_user_refill_perms
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-category"))
    assert request.status_code == 302
    assert "/login" in request.url


# ----------- Items ----------- #
@pytest.mark.django_db
def test_view_create_page_item_with_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_create_page_item_with_item_perms(
    client, create_user_item_perms, create_category, create_image
):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_create_page_item_with_category_perms(
    client, create_user_category_perms
):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_create_page_item_with_refill_perms(
    client, create_user_refill_perms
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:add-item"))
    assert request.status_code == 302
    assert "/login" in request.url


# ----------- Refill ----------- #
@pytest.mark.django_db
def test_view_refill_balance_page_with_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_refill_balance_page_with_item_perms(
    client, create_user_item_perms
):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_refill_balance_page_with_category_perms(
    client, create_user_category_perms
):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_refill_balance_page_with_refill_perms(
    client, create_user_refill_perms
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200


# ----------- Happy Hour ----------- #
@pytest.mark.django_db
def test_view_refill_balance_page_with_all_perms(client, create_user_all_perms):
    user = create_user_all_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200


@pytest.mark.django_db
def test_view_refill_balance_page_with_item_perms(
    client, create_user_item_perms
):
    user = create_user_item_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_refill_balance_page_with_category_perms(
    client, create_user_category_perms
):
    user = create_user_category_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 302
    assert "/login" in request.url


@pytest.mark.django_db
def test_view_refill_balance_page_with_refill_perms(
    client, create_user_refill_perms
):
    user = create_user_refill_perms
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("shop:refill"))
    assert request.status_code == 200


# ----------- User without permissions has nothing to do in admin ----------- #
@pytest.mark.django_db
def test_view_any_admin_related_no_perms(client, create_user_no_perms):
    user = create_user_no_perms
    client.login(username=user.username, password="defaultpassword")
    for urlpattern in urlpatterns:
        url = urlpattern.lookup_str
        if "admin" in url:
            url = reverse(f"shop:{urlpattern.name}")
            request = client.get(url)
            assert request.status_code == 302
            assert "/login" in request.url
