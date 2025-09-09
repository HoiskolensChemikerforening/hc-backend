from django.test import TestCase
from ..forms import GroupForm
from ..models import CGP, Country, Group, Vote
from django.contrib.auth.models import User


class TestForms(TestCase):
    def setUp(self):
        self.cgp = CGP.objects.create(year=1998)
        User.objects.create(username="g", password="f", email="sh@hd.com")
        User.objects.create(username="h", password="hsfd", email="fds@hd.com")
        self.country = Country.objects.create(country_name="heh", slug="heh")
        self.country2 = Country.objects.create(
            country_name="heh2", slug="heh2"
        )

    def test_group_form(self):
        form = GroupForm(
            self.cgp,
            None,
            data={"real_name": "hehe", "country": self.country.id},
        )
        self.assertTrue(form.is_valid())
