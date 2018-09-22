import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_basic_user_admin_page_no_open_election(client, create_user):
    user = create_user

    client.login(username=user.username, password='defaultpassword')

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_start_election'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_end_election'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_register_positions'))
    assert request.status_code == 302
    assert reverse('login') in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse('elections:admin_results'))
    assert request.status_code == 302
    assert reverse('login') in request.url


@pytest.mark.django_db
def test_admin_user_admin_page_no_open_election(client, create_admin_user):
    user = create_admin_user
    client.login(username=user.username, password='defaultpassword')

    # Check that admin user can access start election
    request = client.get(reverse('elections:admin_start_election'))
    assert request.status_code == 200
    assert 'Trykk på Start for å sette igang et valg' in request.content.decode('utf-8')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_end_election'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_register_positions'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')

    # Check that admin user is redirected to start election when election does not exist
    request = client.get(reverse('elections:admin_results'))
    assert request.status_code == 302
    assert request.url == reverse('elections:admin_start_election')
