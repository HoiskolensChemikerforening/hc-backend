from django.db import models
User = settings.AUTH_USER_MODEL


class Candidate(models.Model):
    """docstring for Candidate"""
    postition = models.ForeignKey(Position)
    user = models.ForeignKey(User)
    votes = models.ForeignKey(Ticket, through = 'Vote')

    def __init__(self, arg):
        super(Candidate, self).__init__()
        self.arg = arg

    def __str__(self
        return self.user.name

class Position(models.Model):
    """docstring for Position"""
    name = models.CharField(max_length = 20)
    seats = models.SmallIntegerField()
    active = models.BooleanField(verbose_name="Currently voting")
    def __init__(self, arg):
        super(Position, self).__init__()
        self.arg = arg

    def __str__(self):
        return self.name

class Vote(models.Model):
    """docstring for Vote"""
    def __init__(self, arg):
        super(Vote, self).__init__()
        self.arg = arg

class Ticket(models.Model):
    """docstring for Ticket"""
    def __init__(self, arg):
        super(Ticket, self).__init__()
        self.arg = arg
# Create your models here.
