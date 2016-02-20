from django.db import models
User = settings.AUTH_USER_MODEL

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

class Candidate(models.Model):
    """docstring for Candidate"""
    postition = models.ForeignKey(Position, NULL = False)
    user = models.ForeignKey(user, NULL = False)
    def __init__(self, arg):
        super(Candidate, self).__init__()
        self.arg = arg

class Position(models.Model):
    """docstring for Position"""
    def __init__(self, arg):
        super(Position, self).__init__()
        self.arg = arg



# Create your models here.
