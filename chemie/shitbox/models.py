from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
# Create your models here.

class Submission(models.Model):
    """"
        #This class is supposed to create the shitbox used to
        #send quotes / rumors to Sugepumpen
    """
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length = 2000)
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
