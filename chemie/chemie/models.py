from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from .validators import validate_http


class pictures_for_404(models.Model):
    picture = ImageField(upload_to='404', verbose_name='tullebilde')


class Sponsor(models.Model):
    href = models.CharField(max_length=200, verbose_name="Link", validators=[validate_http])
    start_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    image = ImageField(upload_to='sponsors', verbose_name="Bilde")
    author = models.ForeignKey(User)

    def __str__(self):
        return self.href