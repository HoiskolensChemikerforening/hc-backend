from django.db import models
from uuid import uuid4 as uuid


class Locker(models.Model):
    number = models.PositiveSmallIntegerField()


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    username = models.CharField(max_length=10)
    created = models.DateField(auto_now=False, auto_now_add=True)
    ownerships = models.ManyToManyField(Locker, through='Ownership')


class Ownership(models.Model):
    locker = models.ForeignKey(Locker, related_name="ownerships")
    user = models.ForeignKey(User)
    created = models.DateField(auto_now=False, auto_now_add=True)
    edited = models.DateField(auto_now=True, auto_now_add=False)
    validation_code = models.UUIDField(default=uuid)
    activation_code = models.UUIDField(default=uuid)
    active = models.BooleanField(default=False)








