from django.db import models
from django.contrib.auth.models import User


class Committee(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    #image =

class Member(models.Model):
    committee = models.ForeignKey(Committee)
    user = models.ForeignKey(User)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        user = self.user.all()
        usernames = [thisuser.username for thisuser in user]
        return ', '.join(usernames)
