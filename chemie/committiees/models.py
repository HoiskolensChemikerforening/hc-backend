from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Committee(models.Model):
    name = models.TextField(max_length=100)


class Person(models.Model):
    committee = models.ForeignKey(Committee)
    user = models.ManyToManyField(User)
    startdate = models.CharField(max_length = 20)
    enddate = models.CharField(max_length = 20)

    def __str__(self):
        user = self.user.all()
        usernames = [thisuser.username for thisuser in user]
        return ', '.join(usernames)
