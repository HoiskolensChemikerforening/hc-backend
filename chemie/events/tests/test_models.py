from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time
from post_office.models import Email

from chemie.customprofile.factories import RandomProfileFactory
from chemie.customprofile.models import GRADES
from .factories import BedpresEventFactory, SocialEventFactory
from ..models import (
    BedpresRegistration,
    SocialEventRegistration,
    REGISTRATION_STATUS,
)
from ..views import BedpresRegisterUserView


@pytest.mark.django_db
def test_registration_lists():
    now = timezone.now()
    bedpres = BedpresEventFactory(
        date=now + timedelta(days=3),
        register_startdate=now,
        register_deadline=now + timedelta(days=1),
        deregister_deadline=now + timedelta(days=2),
        sluts=1,
        allowed_grades=[1, 2],
    )
    profile_one = RandomProfileFactory(grade=GRADES.FIRST)
    profile_two = RandomProfileFactory(grade=GRADES.FIRST)
    reg_one = BedpresRegistration.objects.create(
        event=bedpres, user=profile_one.user
    )
    reg_one.save()
    reg_two = BedpresRegistration.objects.create(
        event=bedpres, user=profile_two.user
    )
    reg_two.save()
    assert reg_one.status == REGISTRATION_STATUS.INTERESTED
    assert reg_two.status == REGISTRATION_STATUS.INTERESTED

    # Test that users are registered as attending when there are free slots
    BedpresRegisterUserView.set_user_event_status(
        event=bedpres, registration=reg_one
    )
    assert reg_one.status == REGISTRATION_STATUS.CONFIRMED

    # Test waiting list functionality
    BedpresRegisterUserView.set_user_event_status(
        event=bedpres, registration=reg_two
    )
    assert reg_two.status == REGISTRATION_STATUS.WAITING

    # Test de-registration functionality
    BedpresRegistration.objects.de_register(reg_one)
    with pytest.raises(BedpresRegistration.DoesNotExist):
        reg_one.refresh_from_db()

    reg_two.refresh_from_db()
    assert reg_one.pk is None
    assert reg_two.status == REGISTRATION_STATUS.CONFIRMED


class TestDateRegistrationCriteria:
    fake_now = "2052-12-01 00:30"

    @freeze_time(fake_now)
    @pytest.mark.django_db
    def test_registration_criteria(self):
        now = timezone.now()
        bedpres = BedpresEventFactory(
            register_startdate=now + timedelta(days=1),
            register_deadline=now + timedelta(days=2),
            deregister_deadline=now + timedelta(days=3),
            date=now + timedelta(days=4),
            sluts=1,
            allowed_grades=[2],
        )

        # It is not possible to register yet
        assert bedpres.registration_has_opened() is False
        assert bedpres.can_signup is False
        assert bedpres.can_de_register is True

        # It is possible to register when the event has opened
        with freeze_time(now + timedelta(days=1, hours=1)):
            assert bedpres.registration_has_opened() is True
            assert bedpres.can_signup is True

        # It is not possible to register after the registration deadline has passed
        with freeze_time(now + timedelta(days=2, hours=1)):
            assert bedpres.registration_has_opened() is True
            assert bedpres.can_signup is False

        # It is not possible to de-register after the de-registration deadline
        with freeze_time(now + timedelta(days=3, hours=1)):
            assert bedpres.can_de_register is False


@pytest.mark.django_db
def test_grade_guarding():
    now = timezone.now()
    bedpres = BedpresEventFactory(
        date=now + timedelta(days=3),
        register_startdate=now,
        register_deadline=now + timedelta(days=1),
        deregister_deadline=now + timedelta(days=2),
        sluts=1,
        allowed_grades=[2],
    )
    profile_with_correct_grade = RandomProfileFactory(grade=2)
    profile_with_incorrect_grade = RandomProfileFactory(grade=3)

    # A profile with correct grade can sign up, while an incorrect one can't
    assert bedpres.allowed_grade(profile_with_correct_grade.user) is True
    assert bedpres.allowed_grade(profile_with_incorrect_grade.user) is False


@freeze_time("2052-12-01 00:30")
@pytest.mark.django_db
def test_signup_email():
    call_command("loaddata", "./fixtures/email-templates.json")

    now = timezone.now()
    bedpres = BedpresEventFactory(
        date=now + timedelta(days=3),
        register_startdate=now,
        register_deadline=now + timedelta(days=1),
        deregister_deadline=now + timedelta(days=2),
        sluts=0,
        allowed_grades=[1],
    )
    user_profile = RandomProfileFactory(grade=1)
    registration = BedpresRegistration.objects.create(
        event=bedpres, user=user_profile.user
    )
    registration.save()
    set_user_event_status(event=bedpres, registration=registration)
    bedpres.sluts = 1
    bedpres.save()
    registration.refresh_from_db()
    emails = Email.objects.all()
    email = emails.first()

    # An email is sent and it contains the relevant information
    assert registration.status == REGISTRATION_STATUS.CONFIRMED
    assert emails.count() == 1

    assert bedpres.location in email.message
    assert bedpres.location in email.html_message
    assert "Du er påmeldt" in email.message
    assert "Du er påmeldt" in email.html_message
    # Notice that the dates are 1 hour off the frozen time
    # This is due to the timezone settings
    assert "3. desember - 01:30" in email.message
    assert "3. desember - 01:30" in email.html_message
    assert "4. desember - 01:30" in email.message
    assert "4. desember - 01:30" in email.html_message


@pytest.mark.django_db
def test_social_event_attendee_count():
    now = timezone.now()
    social = SocialEventFactory(
        date=now + timedelta(days=3),
        register_startdate=now,
        register_deadline=now + timedelta(days=1),
        deregister_deadline=now + timedelta(days=2),
        sluts=1,
        allowed_grades=[1, 2],
        companion=True,
    )
    profile = RandomProfileFactory(grade=GRADES.FIRST)
    registration = SocialEventRegistration.objects.create(
        event=social, user=profile.user, companion="Someone"
    )
    registration.save()
    set_user_event_status(event=social, registration=registration)
    assert social.registered_users() == 2
