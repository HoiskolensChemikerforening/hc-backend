import pytest
from django.shortcuts import reverse
from



@pytest.mark.django_db
def test_user_not_logged_in(client,create_user):
    request = client.get(reverse('elections:vote'))
    assert request.status_code == 302
    assert reverse('login') in request.url

@pytest.mark.django_db
def test_election_not_open(client,create_user):
    user = create_user
    client.login(username=user.username, password='defaultpassword')

    request = client.get(reverse('elections:vote'))
    assert "Valget har ikke åpnet enda" in request.content.decode('utf-8')
    assert '<a class="button" href="/elections/results">' in request.content.decode('utf-8')

    request = client.get(reverse('elections:has_voted'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url
    request = client.get(reverse('elections:voting'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url


@pytest.mark.django_db
def test_election_is_open(client,create_user, create_election_with_positions):
    election, positions = create_election_with_positions
    election = Election.objects.create()
    client.login(username=user.username, password='defaultpassword')
    request = client.get(reverse('elections:vote'))
    assert reverse('elections:vote') == request.url
    assert "Klargjøres til valg" in request.content.decode('utf-8')

    request = client.get(reverse('elections:has_voted'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url
    request = client.get(reverse('elections:voting'))
    assert request.status_code == 302
    assert reverse('elections:vote') == request.url




