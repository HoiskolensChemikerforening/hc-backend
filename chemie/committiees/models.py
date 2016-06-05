from django.db import models
from django.contrib.auth.models import User
from customprofile.models import Profile

class Committee(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    #image =
    def __str__(self):
        return self.title

class Member(models.Model):
    committee = models.ForeignKey(Committee)
    user = models.ForeignKey(Profile.user)
    start = models.DateTimeField()
    end = models.DateTimeField()
    position_info = models.CharField(max_length=150, default= None)


    def __str__(self):
        name = [self.user.first_name, self.user.last_name]
        return ' '.join(name)
