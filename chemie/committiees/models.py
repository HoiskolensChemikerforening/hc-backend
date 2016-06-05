from django.db import models
from customprofile.models import Profile


class Committee(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    #image =
    def __str__(self):
        return self.title


class Member(models.Model):
    committee = models.ForeignKey(Committee)
    user = models.ForeignKey(Profile)
    start = models.DateTimeField()
    end = models.DateTimeField()
    position_info = models.CharField(max_length=150, default="Medlem")

    def __str__(self):
        return str(self.user)
