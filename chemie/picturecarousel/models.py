from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

class Picture(models.Model):
	picture = ImageField(upload_to='kontorbilder')
	description = models.TextField(max_length=2000, verbose_name='Description')
	approved = models.BooleanField(default=True, verbose_name="Approved")
	author = models.ForeignKey(User, verbose_name='Author')
	date = models.DateTimeField(auto_now_add=True)
