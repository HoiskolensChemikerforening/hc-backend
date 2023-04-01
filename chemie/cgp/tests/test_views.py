from django.test import TestCase, Client
from django.urls import reverse
from ..models import CGP, Group, Country, Vote
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="hei", password="du", email="hei@du.com")
        self.index_url = reverse('cgp:index')
        self.cgp = CGP.create_new_cgp()
        self.country = Country.objects.create(country_name="A", slug="a")
        self.group = Group.objects.create(real_name="d", country=self.country, song_name="f", cgp=self.cgp)
        self.group.group_leaders.add(self.user)
        self.vote_index_url = reverse('cgp:vote_index', args=[self.country.slug])


    def test_index_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cgp/index.html')

    def test_vote_index_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.vote_index_url)
        self.assertEquals(response.status_code, 404)
        self.cgp.is_open = True
        self.cgp.save()
        response = self.client.get(self.vote_index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cgp/vote_index.html')