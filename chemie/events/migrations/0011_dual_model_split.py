from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Count, Q


def make_all_access_cards_unique(app, schema_editor):
    try:
        Event = app.get_model('events', 'Event')
        EventRegistration = app.get_model('events', 'EventRegistration')
    except LookupError:
        print("Old model is no longer installed")
        return

    previous_events = Event.objects.all()

    for event in previous_events:
        attendees = EventRegistration.objects.filter(event=event)
