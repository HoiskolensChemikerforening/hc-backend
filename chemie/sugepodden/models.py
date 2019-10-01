from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from sorl.thumbnail import ImageField



# Create your models here.

class Podcast(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(verbose_name="beskrivelse", config_name="news")
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="Images", verbose_name="Bilde")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name="Publisert")
    url_number = models.URLField(
        name = ("Url Number"),
        max_length=128,
        db_index=True,
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sugepodden:detail_podcast", kwargs={"pk": self.pk})

    def get_absolute_registration_url(self):
        return reverse("sugepodden:register_podcast", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse("sugepodden:delete_podcast", kwargs={"pk": self.pk})


