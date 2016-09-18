from django.db import models
from sorl.thumbnail import ImageField

class pictures_for_404(models.Model):
    picture = ImageField(upload_to='404', verbose_name='tullebilde')