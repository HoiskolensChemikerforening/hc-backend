from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
# Create your models here.

class Submission(forms.Form):
    """"
        #This class is supposed to create the shitbox used to
        #send quotes / rumors to Sugepumpen
    """
    text = forms.CharField(label = 'Ditt sladder', max_length = 2000)
