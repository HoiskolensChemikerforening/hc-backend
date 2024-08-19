import pytest
from django.shortcuts import reverse
from freezegun import freeze_time

from .factories import BedpresEventFactory
from .factories import SocialEventFactory

from ..models import (
    SocialEventRegistration,
    BedpresRegistration,
    REGISTRATION_STATUS,
)


@freeze_time("2040-12-01 00:30")
@pytest.mark.django_db
def test_overview_social(client, create_user):
    future_social = SocialEventFactory.create(title="Altair event")
    user = create_user
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("events:index_social"))
    assert future_social.title in request.content.decode("utf-8")
    assert (
        "Det er ingen aktive sosiale arrangementer"
        not in request.content.decode("utf-8")
    )

    with freeze_time("2040-12-24 00:30"):
        client.login(username=user.username, password="defaultpassword")
        request = client.get(reverse("events:past_social"))
        assert future_social.title in request.content.decode("utf-8")
        request = client.get(reverse("events:index_social"))
        assert (
            "Det er ingen aktive sosiale arrangementer"
            in request.content.decode("utf-8")
        )


@freeze_time("2040-12-01 00:30")
@pytest.mark.django_db
def test_overview_bedpres(client, create_user):
    future_bedpres = BedpresEventFactory.create(title="Altair event")
    user = create_user
    client.login(username=user.username, password="defaultpassword")
    request = client.get(reverse("events:index_bedpres"))
    assert future_bedpres.title in request.content.decode("utf-8")
    assert (
        "Det er ingen aktive arrangementer nå. Finn på noe kult da vel!"
        not in request.content.decode("utf-8")
    )

    with freeze_time("2040-12-24 00:30"):
        client.login(username=user.username, password="defaultpassword")
        request = client.get(reverse("events:past_bedpres"))
        assert future_bedpres.title in request.content.decode("utf-8")

        request = client.get(reverse("events:index_bedpres"))
        assert (
            "Det er ingen aktive arrangementer nå. Finn på noe kult da vel!"
            in request.content.decode("utf-8")
        )


@pytest.mark.django_db
def test_my_active_events(client, create_user):
    social = SocialEventFactory.create(title="Altair event")
    bedpres = BedpresEventFactory.create(title="Altair bedpres")
    user = create_user
    client.login(username=user.username, password="defaultpassword")
    request_social = client.get(reverse("events:index_social"))
    request_bedpres = client.get(reverse("events:index_bedpres"))

    ####### USER NOT ENROLLED #######
    # Test that user does not see any social events when he is not enrolled
    assert (
        "Du er ikke påmeldt noen sosiale arrangementer. Finn på noe sprell!"
        or "Vennligst logg inn for å se dine aktive sosiale arrangementer."
        in request_social.content.decode("utf-8")
    )

    # Test that user does not see any bedpres events when he is not enrolled
    assert (
        "Du er ikke påmeldt noen bedpreser. Finn på noe sprell!"
        or "Vennligst logg inn for å se dine aktive bedpreser."
        in request_bedpres.content.decode("utf-8")
    )

    # Check SQL entry in database
    assert not SocialEventRegistration.objects.filter(
        event=social, user=user
    ).exists()
    assert not BedpresRegistration.objects.filter(
        event=bedpres, user=user
    ).exists()

    ####### ENROLL USER #######
    SocialEventRegistration.objects.create(
        user=user, event=social, status=REGISTRATION_STATUS.CONFIRMED
    )
    BedpresRegistration.objects.create(
        user=user, event=bedpres, status=REGISTRATION_STATUS.CONFIRMED
    )
    # Refetch urls, user is now enrolled
    request_social = client.get(reverse("events:index_social"))
    request_bedpres = client.get(reverse("events:index_bedpres"))

    # Test that user sees his social events when he is enrolled
    assert social.title in request_social.content.decode("utf-8")

    # Test that user sees his bedpres events when he is enrolled
    assert bedpres.title in request_bedpres.content.decode("utf-8")

    # Check SQL entry in database
    assert SocialEventRegistration.objects.filter(
        event=social, user=user
    ).exists()
    assert BedpresRegistration.objects.filter(
        event=bedpres, user=user
    ).exists()


# TODO: Create this test. Should check that all details related to the event is correct and that the HTML displays correctly
@pytest.mark.django_db
def test_create_social_event_view(admin_client):
    url = reverse("events:create_social")
    form_data = {"title": "Bedpres title"}
    # admin_client.post(url, )
    pass
