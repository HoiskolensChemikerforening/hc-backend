import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from chemie.chemie import settings
from chemie.customprofile.factories import RandomProfileFactory
from chemie.events.models import Social, SocialEventRegistration
from ..views import SocialRegisterUserView


# Create your tests here.


class TestEventAndRegistration(TestCase):
    # Fetch all templates for sending mail
    fixtures = ["fixtures/email-templates.json"]

    def setUp(self):
        user = User.objects.create(username="glenny")
        date = timezone.now() + timezone.timedelta(days=5)
        start_date = timezone.now()
        reg_deadline = timezone.now() + timezone.timedelta(days=1)
        dereg_deadline = timezone.now() + timezone.timedelta(days=2)
        image_path = (
            settings.BASE_DIR + "media" + "events" + "blank_person.png"
        )
        image = File(image_path)
        Social.objects.create(
            title="Indok er helt ok",
            author=user,
            date=date,
            register_startdate=start_date,
            register_deadline=reg_deadline,
            deregister_deadline=dereg_deadline,
            location="Samfundet",
            description="Litta fest",
            image=image,
            sluts=10,
            payment_information="Alle maa benytte Vipps til aa betale",
            allowed_grades=[1, 2, 3, 4, 5, 6],
        )

    def test_event_registration_exceeding_max_slots(self):
        event = Social.objects.get(title="Indok er helt ok")
        for i in range(event.sluts + 5):
            profile = RandomProfileFactory.create()
            profile.save()
            registration = SocialEventRegistration(
                event=event, user=profile.user
            )
            SocialRegisterUserView.set_user_event_status(event, registration)
            registration.save()
            # Bumping all users on wait list by
            # calling overridden save function
            event.save()
        self.assertEqual(event.waiting_users(), 5)
        self.assertEqual(event.registered_users(), event.sluts)
