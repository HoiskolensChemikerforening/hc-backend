from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Post(models.Model):
    """"
        #This class is supposed to create the shitbox used to
        #send quotes / rumors to Sugepumpen
    """
    author = models.ForeignKey(User)
    date_submitted = models.DateTimeField(auto_now_add = True)
    date_tampered_with = models.DateTimeField(auto_now = True)
    text = models.CharField(max_length = 2000)
    def __init__(self, arg):

        super(Post, self).__init__()
        self.arg = arg
