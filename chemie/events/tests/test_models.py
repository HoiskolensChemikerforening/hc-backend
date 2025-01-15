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
    SocialResellReceipt,
)
from ..views import set_user_event_status


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
    set_user_event_status(event=bedpres, registration=reg_one)
    assert reg_one.status == REGISTRATION_STATUS.CONFIRMED

    # Test waiting list functionality
    set_user_event_status(event=bedpres, registration=reg_two)
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
    call_command("loaddata", "chemie/fixtures/email-templates.json")

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


@pytest.mark.django_db
def test_social_resell_receipt():
    now = timezone.now()
    # Create Social with 2 slots
    social = SocialEventFactory(
        date=now + timedelta(days=3),
        register_startdate=now,
        register_deadline=now + timedelta(days=1),
        deregister_deadline=now + timedelta(days=2),
        sluts=2,
        allowed_grades=[1, 2],
        companion=False,
    )
    
    # Create 6 users and registrer for the event (2 slots + 4 in queue)
    registrations = []
    profiles = []
    for i in range(6):
        profile = RandomProfileFactory(grade=GRADES.FIRST)
        registration = SocialEventRegistration.objects.create(
            event=social, user=profile.user
        )
        registration.save()
        set_user_event_status(event=social, registration=registration)
        registrations.append(registration)
        profiles.append(profile)


    # Create a resell object on behalv of the first registert user
    # The buyer is set to the 3rd profile (1 in queue) during save()
    resell_receipt = SocialResellReceipt() 
    resell_receipt.response_time = timezone.timedelta(hours=1)
    resell_receipt.seller_registration = registrations[0]
    resell_receipt.save()

    # Create a resell object on behalv of the second registert user
    # The buyer is set to the 4th profile (2 in queue since number one has been offered a slot) during save()
    resell_receipt2 = SocialResellReceipt() 
    resell_receipt2.response_time = timezone.timedelta(hours=1)
    resell_receipt2.seller_registration = registrations[1]
    resell_receipt2.save()

    # Check that the 3rd user has been offered the 1 slot
    assert resell_receipt.buyer_registration == registrations[2]
    # Ensure that both tickets are not offered to the same person
    assert resell_receipt.buyer_registration != resell_receipt2.buyer_registration

    # Retrive the attendees of the social
    attendees = social.attendees.through.objects.filter(
        status=REGISTRATION_STATUS.CONFIRMED, event=social
    )

    # Check that the 1st and 2nd user still have their slots since the purchace has not been completet.
    assert attendees[0].user == profiles[0].user
    assert attendees[1].user == profiles[1].user

    # Offer the slot of the 1st person to the 5th person (next in queue) assuming that the 3rd person did not respond.
    resell_receipt.offer()
    assert resell_receipt.buyer_registration == registrations[4]

    # Sell the spot of the 1st person to the 5th person.
    resell_receipt.sell()

    # Confirm the payment 
    resell_receipt.confirm_payment()

    attendees = social.attendees.through.objects.filter(
            status=REGISTRATION_STATUS.CONFIRMED, event=social
        )

    # Check if the 5th user received the slot of the 1st user. 
    assert attendees[1].user == profiles[4].user
    # Check if the 2nd user still has its slot.
    assert attendees[0].user == profiles[1].user




