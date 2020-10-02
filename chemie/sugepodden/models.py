from django.db import models

# Create your models here.
from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.urls import reverse

class Podcast(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField(max_length=200, verbose_name="beskrivelse")
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="sugepodden", verbose_name="Bilde", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name="Publisert")
    url = models.URLField(max_length=200, default="")

    def __str__(self):
        return self.title

    def get_absolute_delete_url(self):
        return reverse(
            reverse("sugepodden:delete_podcast", kwargs={"pk": self.pk})
        )


