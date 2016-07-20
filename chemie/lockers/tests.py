from django.test import TestCase
from lockers.models import *

def LockerUserTestCase(TestCase):
    def setUp(self):
        LockerUser.objects.create(first_name="Jöns Jacob",
                                  last_name="Berzelius",
                                  username='jzelius')
