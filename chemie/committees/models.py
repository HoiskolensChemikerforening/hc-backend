from django.db import models
from customprofile.models import Profile


class Committee(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    #image =

    def __str__(self):
        return self.title


class Position(models.Model):
    position_name = models.CharField(max_length=100, verbose_name="Stillingsnavn")
    epost = models.EmailField(null=True, blank=True, verbose_name="Epost")
    committee = models.ForeignKey(Committee)

    def __str__(self):
        return str(self.user)

class Member(models.Model):
    position = models.ForeignKey(Position)
    user = models.ForeignKey(Profile)
    start = models.DateTimeField(verbose_name="Startdato")
    end = models.DateTimeField(verbose_name="Sluttdato")