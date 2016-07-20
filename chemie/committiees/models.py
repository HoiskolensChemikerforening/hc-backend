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
    email = models.EmailField(null=True, blank=True, verbose_name="Epost for vervet")
    user = models.ForeignKey(Profile)
    start = models.DateTimeField(verbose_name="Startdato")
    end = models.DateTimeField(verbose_name="Sluttdato")
    position_title = models.CharField(max_length=150, default="Medlem", verbose_name="Tittel på stilling")

    def __str__(self):
        return str(self.user)
