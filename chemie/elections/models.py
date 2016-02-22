from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    """docstring for Position"""
    name = models.CharField(max_length = 20)
    seats = models.SmallIntegerField(verbose_name="Number of seats to be selected")
    active = models.BooleanField(verbose_name="Active position")

    def __str__(self):
        return self.name

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class Ticket(models.Model):
    """docstring for Ticket"""
    secret = models.CharField(max_length = 12)


class Candidate(models.Model):
    """docstring for Candidate"""
    postition = models.ForeignKey(Position)
    users = models.ManyToManyField(User)
    votes = models.ManyToManyField(Ticket, through = 'Vote')

    def __str__(self):
        return self.users.get(id=1).username



class Vote(models.Model):
    """docstring for Vote"""
    candidate = models.ForeignKey(Candidate)
    ticket = models.ForeignKey(Ticket)
    time = models.TimeField(auto_now_add=True)


# Create your models here.
