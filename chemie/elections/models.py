from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

class Election(models.Model):
    name = models.CharField(max_length = 20)
    date = models.DateField(auto_now=True)


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

#class TicketManager(models.Manager):
#    def create_ticket(self, secret):
#        ticket = self.create(secret=secret)
#        return ticket

class Ticket(models.Model):
    """docstring for Ticket"""
    secret = models.CharField(max_length = 12, unique = True)
    #objects = TicketManager()

class Candidate(models.Model):
    """docstring for Candidate"""
    postition = models.ForeignKey(Position)
    users = models.ManyToManyField(User)
    votes = models.ManyToManyField(Ticket, through = 'Vote')

    def __str__(self):
        users = self.users.all()
        usernames = [user.username for user in users]
        return ', '.join(usernames)


class Vote(models.Model):
    """docstring for Vote"""
    candidate = models.ForeignKey(Candidate)
    ticket = models.ForeignKey(Ticket)
    time = models.TimeField(auto_now_add=True)

    @transaction.atomic
    def add_vote(request):
        pass
# Create your models here.
