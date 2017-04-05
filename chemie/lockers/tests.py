from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from lockers.models import LOCKER_COUNT
from lockers.models import LockerUser, Locker, LockerToken, Ownership


def create_user_with_locker(count):
    user = LockerUser.objects.create(first_name="Glenn",
                                     last_name="Gregor",
                                     email='glenny')
    for i in range(count):
        locker = Locker.objects.create(number=i)
        ownership = Ownership.objects.create(locker=locker, user=user)
        token = LockerToken.objects.create(ownership=ownership)
        token.activate()


class LockerUserLimitTest(TestCase):
    def setUp(self):
        create_user_with_locker(LOCKER_COUNT-1)

    def test_not_reached_limit(self):
        ownership = Ownership.objects.filter(user__email='glenny')[0]
        self.assertEqual(ownership.reached_limit(), False)

    def test_reached_limit(self):
        ownership = Ownership.objects.filter(user__email='glenny')[0]
        user = ownership.user

        locker = Locker.objects.create(number=LOCKER_COUNT)
        ownership = Ownership.objects.create(locker=locker, user=user)
        token = LockerToken.objects.create(ownership=ownership)
        token.activate()

        self.assertEqual(ownership.reached_limit(), True)


class TokenTest(TestCase):
    def setUp(self):
        user = LockerUser.objects.create(first_name="Glenn",
                                         last_name="Gregor",
                                         email='glenny')
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
