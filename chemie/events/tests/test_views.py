from datetime import timedelta
from .factories import SocialEventFactory
import pytest
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time
from post_office.models import Email
from django.shortcuts import reverse

from customprofile.factories import RandomProfileFactory
from customprofile.models import GRADES
from .factories import BedpresEventFactory
from ..models import BedpresRegistration, REGISTRATION_STATUS
from ..views import set_user_event_status





@freeze_time('2040-12-01 00:30')
@pytest.mark.django_db
def test_overview_social(client_profile):
    future_social = SocialEventFactory.create(title="Altair event")
    request = client_profile.get(reverse('events:index_social'))
    assert future_social.title in request.content.decode('utf-8')
    assert "Det er ingen aktive sosiale arrangementer" not in request.content.decode('utf-8')

    with freeze_time('2040-12-24 00:30'):
        request = client_profile.get(reverse('events:past_social'))
        assert future_social.title in request.content.decode('utf-8')

        request = client_profile.get(reverse('events:index_social'))
        assert "Det er ingen aktive sosiale arrangementer" in request.content.decode('utf-8')


@freeze_time('2040-12-01 00:30')
@pytest.mark.django_db
def test_overview_bedpres(client_profile):
    future_bedpres = BedpresEventFactory.create(title="Altair event")
    request = client_profile.get(reverse('events:index_bedpres'))
    assert future_bedpres.title in request.content.decode('utf-8')
    assert "Det er ingen aktive bedpresser" not in request.content.decode('utf-8')

    with freeze_time('2040-12-24 00:30'):
        request = client_profile.get(reverse('events:past_bedpres'))
        assert future_bedpres.title in request.content.decode('utf-8')

        request = client_profile.get(reverse('events:index_bedpres'))
        assert "Det er ingen aktive bedpreser nå" in request.content.decode('utf-8')


@pytest.mark.django_db
def test_my_active_social_events(client_profile):
    social = SocialEventFactory.create(title="Altair event")

    request = client_profile.get(reverse('events:index_social'))


#    my_event = SocialEventFactory.create()

# Create social event
# Create bedbres




@pytest.mark.django_db
def test_create_social_event_view(admin_client):
    url = reverse('events:create_social')
    form_data = {
        'title':'Bedpres title',
    }
    #admin_client.post(url, )
    pass
