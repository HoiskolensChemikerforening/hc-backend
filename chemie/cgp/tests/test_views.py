from django.test import TestCase, Client
from django.urls import reverse
from ..models import CGP, Group, Country, Vote
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="hei", password="du", email="hei@du.com"
        )
        self.index_url = reverse("cgp:index")
        self.cgp = CGP.create_new_cgp()
        self.country = Country.objects.create(country_name="A", slug="a")
        self.group = Group.objects.create(
            real_name="d", country=self.country, song_name="f", cgp=self.cgp
        )
        self.group.group_leaders.add(self.user)
        self.vote_index_url = reverse(
            "cgp:vote_index", args=[self.country.slug]
        )

    def test_index_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "cgp/index.html")

    def test_vote_index_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.vote_index_url)
        self.assertRedirects(
            response, "/cgp", status_code=302, target_status_code=301
        )
        self.cgp.is_open = True
        self.cgp.save()
        response = self.client.get(self.vote_index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "cgp/vote_index.html")


class TestViewsWithLargerDataBase(TestCase):
    def setUp(self):
        self.client = Client()
        users = [
            "1u",
            "2u",
            "3u",
            "4u",
            "5u",
            "6u",
            "7u",
            "8u",
            "9u",
            "10u",
            "11u",
            "12u",
            "13u",
            "14u",
            "15u",
            "16u",
            "17u",
        ]
        self.users = [
            User.objects.create_user(
                username=u, password=u, email=f"{u}@{u}.com"
            )
            for u in users
        ]

        self.cgp = CGP.create_new_cgp()
        countries = [
            "1c",
            "2c",
            "3c",
            "4c",
            "5c",
            "6c",
            "7c",
            "8c",
            "9c",
            "10c",
            "11c",
            "12c",
            "13c",
            "14c",
            "15c",
            "16c",
            "17c",
        ]
        self.countrys = [
            Country.objects.create(country_name=c, slug=c) for c in countries
        ]
        groups = [
            "1g",
            "2g",
            "3g",
            "4g",
            "5g",
            "6g",
            "7g",
            "8g",
            "9g",
            "10g",
            "11g",
            "12g",
            "13g",
            "14g",
            "15g",
            "16g",
            "17g",
        ]
        songs = [
            "1s",
            "2s",
            "3s",
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "10s",
            "11s",
            "12s",
            "13s",
            "14s",
            "15s",
            "16s",
            "17s",
        ]
        self.groups = [
            Group.objects.create(
                real_name=groups[index],
                country=self.countrys[index],
                song_name=songs[index],
                cgp=self.cgp,
            )
            for index, g in enumerate(groups)
        ]
        self.votes = []
        for index, group in enumerate(self.groups):
            group.group_leaders.add(self.users[index])

        self.groups[0].audience = True
        self.groups[0].save()
        voteList = [
            [
                self.users[:8],
                '["1c,2c,3c,4c,5c,6c,7c,8c,9c,10c,11c,12c,13c,14c,15c,16c,17c"]',
                1,
                2,
            ],
            [
                self.users[8:16],
                '["2c,1c,4c,3c,5c,6c,7c,8c,9c,10c,11c,12c,13c,14c,15c,16c,17c"]',
                1,
                2,
            ],
            [
                self.users[16:],
                '["4c,3c,1c,2c,5c,6c,7c,8c,9c,10c,11c,12c,13c,14c,15c,16c,17c"]',
                3,
                4,
            ],
        ]
        # Points                 184 183 130 132
        def generateVotes(array, voteString, fiaskovoteindex, showvoteindex):
            for u in array:
                vote = Vote.objects.create(
                    final_vote=False,
                    group=self.groups[0],
                    user=u,
                    vote=voteString,
                    failureprize_vote=self.groups[fiaskovoteindex],
                    showprize_vote=self.groups[showvoteindex],
                )
                self.votes.append(vote)

        for votelst in voteList:
            array, voteString, fiaskovoteindex, showvoteindex = votelst
            generateVotes(array, voteString, fiaskovoteindex, showvoteindex)

    def test_close_election(self):
        self.cgp.toggle(self.users[0])
        self.cgp.toggle(self.users[0])
        audiencevote = Vote.objects.get(final_vote=True, group__audience=True)
        self.assertEquals(audiencevote.vote[:11], "1c,2c,4c,3c")
