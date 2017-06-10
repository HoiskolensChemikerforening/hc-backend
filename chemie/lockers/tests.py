from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from lockers.models import LOCKER_COUNT
from lockers.models import LockerUser, Locker, LockerToken, Ownership
from lockers.management.commands.resetlockerstatus import reset_locker_ownerships


def create_user_with_locker(count):
    user = LockerUser.objects.create(first_name="Glenn",
                                     last_name="Gregor",
                                     email='glenny@test.no')
    for i in range(count):
        locker = Locker.objects.create(number=i)
        ownership = Ownership.objects.create(locker=locker, user=user)
        token = LockerToken.objects.create(ownership=ownership)
        token.activate()


class LockerUserLimitTest(TestCase):
    def setUp(self):
        create_user_with_locker(LOCKER_COUNT-1)

    def test_not_reached_limit(self):
        ownership = Ownership.objects.filter(user__email='glenny@test.no')[0]
        self.assertEqual(ownership.reached_limit(), False)

    def test_reached_limit(self):
        ownership = Ownership.objects.filter(user__email='glenny@test.no')[0]
        user = ownership.user

        locker = Locker.objects.create(number=LOCKER_COUNT)
        ownership = Ownership.objects.create(locker=locker, user=user)
        token = LockerToken.objects.create(ownership=ownership)
        token.activate()

        self.assertEqual(ownership.reached_limit(), True)


class TokenTest(TestCase):
    # Fetch all templates for sending mail
    fixtures = ['fixtures/email-templates.json']
    def setUp(self):
        user = LockerUser.objects.create(first_name="Glenn",
                                         last_name="Gregor",
                                         email='glenny@test.no')
        locker = Locker.objects.create(number=1)
        ownership = Ownership.objects.create(locker=locker, user=user)
        token = LockerToken.objects.create(ownership=ownership)

    def test_locker_inactive(self):
        locker = Locker.objects.get(number=1)
        ownership = Ownership.objects.get(locker=locker)
        self.assertEqual(locker.is_free(), True)
        self.assertEqual(ownership.is_active, False)
        self.assertEqual(ownership.is_confirmed, False)

    def test_locker_taken(self):
        locker = Locker.objects.get(number=1)
        ownership = Ownership.objects.get(locker=locker)
        token = LockerToken.objects.get(ownership=ownership)
        token.activate()

        ownership = Ownership.objects.get(locker=locker)
        locker = Locker.objects.get(number=1)

        self.assertEqual(locker.is_free(), False)
        self.assertEqual(ownership.is_active, True)
        self.assertEqual(ownership.is_confirmed, True)
        self.assertEqual(token.pk, None)

    def test_prune_expired(self):
        locker = Locker.objects.get(number=1)
        ownership = Ownership.objects.get(locker=locker)
        token = LockerToken.objects.get(ownership=ownership)
        # Locker was tried taken without confirming 8 days ago
        token.created = timezone.now() - timedelta(days=8)
        token.save()
        LockerToken.objects.prune_expired()
        # Try to get the recently pruned locker token,
        # but it raises an object does not exist since it was just pruned.
        self.assertRaises(ObjectDoesNotExist, LockerToken.objects.get, ownership=ownership)

    def test_reset_idle(self):
        locker = Locker.objects.get(number=1)
        user = LockerUser.objects.get(email='glenny@test.no')
        ownership = Ownership.objects.get(locker=locker, user=user)
        token = LockerToken.objects.get(ownership=ownership)
        token.activate()

        ownership.refresh_from_db()
        ownership.is_active = False
        ownership.save()
        Locker.objects.reset_idle()
        locker.refresh_from_db()
        self.assertEqual(locker.owner, None)
        self.assertEqual(locker.number, 1)
        self.assertEqual(user.email, 'glenny@test.no')
        self.assertEqual(ownership.locker.number, 1)
        self.assertEqual(ownership.user.email, 'glenny@test.no')


    def test_reset_locker_ownerships(self):
        # Fetch locker, user, ownership and attach locker <=> ownership
        locker = Locker.objects.get(number=1)
        user = LockerUser.objects.get(email='glenny@test.no')
        ownership = Ownership.objects.get(locker=locker,
                                          user=user)
        token = LockerToken.objects.get(ownership=ownership)
        token.activate()
        locker.refresh_from_db()
        ownership.refresh_from_db()
        # Check if ownership points to locker and vice versa
        self.assertEqual(locker.owner, ownership)
        self.assertEqual(ownership.locker, locker)
        self.assertEqual(ownership.is_active, True)
        self.assertEqual(ownership.is_confirmed, True)
        # Try to cut the link from ownership to locker
        # (set is_active = False)
        reset_locker_ownerships()
        locker.refresh_from_db()
        user.refresh_from_db()
        ownership.refresh_from_db()
        # Check if the only change made was cutting ownership to locker
        # (is_active = False)
        self.assertEqual(ownership.is_active, False)
        self.assertEqual(ownership.is_confirmed, True)
        self.assertEqual(locker.owner, ownership)
        self.assertEqual(ownership.locker, locker)

        token = LockerToken.objects.create(ownership=ownership)
        token.activate()
        self.assertEqual(ownership.is_active, True)
        self.assertEqual(ownership.is_confirmed, True)
        self.assertEqual(locker.owner, ownership)
        self.assertEqual(ownership.locker, locker)
