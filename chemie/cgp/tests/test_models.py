from django.test import TestCase
from ..models import CGP
from django.contrib.auth.models import User
from django.utils import timezone

class CGPTestCase(TestCase):
    def setUp(self):
        self.cgp = CGP.objects.create(year=1995)
        CGP.objects.create(year=2000)
        self.user = User.objects.create(username="Kåre Oh", password="stinkt", email="sehr@doll.com")

    def test_if_get_latest_or_create_returns_latest(self):
        """Tests if get_latest_or_create always returns CGP object"""
        cgp = CGP.get_latest_or_create()
        self.assertEqual(cgp.year, 2000)

    def test_toggle(self):
        self.assertFalse(self.cgp.is_open)
        self.cgp.toggle(self.user)
        self.assertTrue(self.cgp.is_open)