from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField


class Contribution(models.Model):
    image = ImageField(upload_to='kontorbilder')
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.approved = True
        return True
