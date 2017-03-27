from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField


class Submission(models.Model):
    image = ImageField(upload_to='kontorbilder')
    approved = models.BooleanField(default=False, verbose_name="Approved")
    author = models.ForeignKey(User, verbose_name='Author')
    date = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.approved = True
        return True
