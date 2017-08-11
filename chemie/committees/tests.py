from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.test import TestCase, Client

from customprofile.factories import RandomUserFactory
from .factories import LowPermissionPositionFactory, HighPermissionPositionFactory


class PositionTest(TestCase):
    def setUp(self):
        self.usercount = 4
        self.users = [RandomUserFactory.create() for x in range(0, self.usercount)]
        self.low_user, self.high_user, self.no_perms_user = self.users[:3]

        self.low_permission_position = LowPermissionPositionFactory()
        self.high_permission_position = HighPermissionPositionFactory()

        committee = self.low_permission_position.committee
        self.edit_committee = reverse('verv:edit_description', kwargs={'slug': committee.slug})
        self.edit_members = reverse('verv:edit_memberships', kwargs={'slug': committee.slug})

    def login_user(self):
        client_users = [Client() for x in range(0, self.usercount)]
        a = []
        for client, user in zip(client_users, self.users):
            a.append(client.login(username=user.username, password='defaultpassword'))

        self.low_user, self.high_user, self.no_perms_user = client_users[:3]

    def test_position_manage_users(self):
        self.low_permission_position.users.add(self.users[1])
        self.assertEqual(self.users[1] in self.low_permission_position.users.all(), True)
        self.low_permission_position.users.remove(self.users[1])
        self.assertEqual(self.users[0] in self.low_permission_position.users.all(), False)

    def test_position_max_members(self):
        self.assertRaises(ValidationError, self.low_permission_position.users.add, self.users[0], self.users[1])

    def test_position_user_permission_inheritance(self):
        position = self.low_permission_position
        self.assertFalse(self.users[0].has_perm('committees.change_committee'))

        position.users.add(self.users[0])
        user = User.objects.get(pk=self.users[0].pk)
        self.assertTrue(user.has_perm('committees.change_committee'))

        position.users.remove(self.users[0])
        user = User.objects.get(pk=self.users[0].pk)
        self.assertFalse(user.has_perm('committees.change_committee'))

    def test_position_can_manage_committee(self):
        self.login_user()
        response = self.no_perms_user.get(self.edit_committee, follow=False)
        self.assertEqual(response.status_code, 302)

        response = self.no_perms_user.get(self.edit_members, follow=False)
        self.assertEqual(response.status_code, 302)

        self.low_permission_position.users.add(self.users[0])
        self.login_user()
        self.low_permission_position.can_manage_committee = True
        self.low_permission_position.save()

        response = self.low_user.get(self.edit_committee, follow=True)
        self.assertContains(response, '<!-- Edit committee page -->')
        response = self.low_user.get(self.edit_members, follow=True)
        self.assertContains(response, '<!-- Edit committee members -->')

    def test_super_position_can_manage_committee(self):
        self.high_permission_position.users.add(self.high_user)
        self.login_user()
        response = self.high_user.get(self.edit_members, follow=True)
        self.assertContains(response, '<!-- Edit committee members -->')

    def test_delete_position(self):
        self.low_permission_position.users.add(self.low_user)
        user = User.objects.get(pk=self.low_user.pk)
        self.assertTrue(user.has_perm('committees.change_committee'))
        self.low_permission_position.delete()
        user = User.objects.get(pk=self.low_user.pk)
        self.assertFalse(user.has_perm('committees.change_committee'))

    def test_delete_committee(self):
        self.low_permission_position.users.add(self.low_user)
        user = User.objects.get(pk=self.low_user.pk)
        self.assertTrue(user.has_perm('committees.change_committee'))
        self.low_permission_position.committee.delete()
        user = User.objects.get(pk=self.low_user.pk)
        self.assertFalse(user.has_perm('committees.change_committee'))
