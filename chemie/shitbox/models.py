from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class Submission(models.Model):
    content = models.TextField(max_length=2000, verbose_name='Sladder')
    image = ImageField(upload_to='shitbox', blank=True, null=True, verbose_name="Bilde")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Innsender')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
