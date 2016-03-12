from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
# Create your models here.


class Submission(models.Model):
    """docstring for submission"""
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length = 2000)
    time = models.TimeField(auto_now_add=True)
