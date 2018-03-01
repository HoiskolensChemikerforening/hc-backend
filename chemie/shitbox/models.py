from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Submission(models.Model):
    content = models.TextField(max_length=2000, verbose_name='Sladder')
    image = ImageField(upload_to='shitbox', blank=True, null=True, verbose_name="Bilde")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Innsender', on_delete=models.CASCADE)
