from django.db import models
from uuid import uuid4 as uuid
from django.contrib.auth.models import User


class Locker(models.Model):
    number = models.PositiveSmallIntegerField()


class LockerUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=10)
    created = models.DateField(auto_now=False, auto_now_add=True)
    internal_user = models.ForeignKey(User)
    ownerships = models.ManyToManyField(Locker, through='Ownership')


class Ownership(models.Model):
    locker = models.ForeignKey(Locker)
    user = models.ForeignKey(LockerUser)
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    activation_code = models.UUIDField(default=uuid)
    active = models.BooleanField(default=False)
