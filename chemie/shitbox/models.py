from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
# Create your models here.


class Submission(models.Model):
    """docstring for submission"""
    content = models.TextField(max_length = 2000)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name = 'Innsender')
