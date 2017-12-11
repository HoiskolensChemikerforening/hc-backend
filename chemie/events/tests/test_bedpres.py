import pytest
import freezegun

@pytest.mark.django_db
def test_create_bedpres():
    # Tests the create bedpres view
    pass

@pytest.mark.django_db
def test_registration_lists():
    # Test that users are registered as attending when there are free slots
    # Test waiting list functionality
    pass

@pytest.mark.django_db
def test_registration_criteria():
    # Test registration_has_opened (used in template)
    # Test can_signup
    pass


@pytest.mark.django_db
def test_grade_guarding(logged_in_client):
    pass


@pytest.mark.django_db
def test_signup_email(mailoutbox):
    # Test that the signup email contains the necessary information
    pass


@pytest.mark.django_db
def test_de_register():
    # Test that de-registration bumps the next user in the waiting list to the attendee list
    pass
