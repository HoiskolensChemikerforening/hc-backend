from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class Podcast(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField(max_length=200, verbose_name="beskrivelse")
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(
        upload_to="sugepodden", verbose_name="Bilde", blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name="Publisert")
    url = models.URLField(max_length=200, default="")

    def __str__(self):
        return self.title

    def get_absolute_delete_url(self):
        return reverse("sugepodden:delete_podcast", kwargs={"pk": self.id})

    @classmethod
    def get_latest_podcast_url(cls):
        try:
            latest_object = cls.objects.latest("id")
            latest_url = latest_object.url
        except ObjectDoesNotExist:
            latest_url = "/sugepodden"

        return latest_url
