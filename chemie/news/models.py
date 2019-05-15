from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from sorl.thumbnail import ImageField
from chemie.web_push.models import Device
from chemie.customprofile.models import Profile

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    content = RichTextField(verbose_name="Beskrivelse", config_name="news")
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="news", verbose_name="Bilde")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name="Publisert")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "news:detail", kwargs={"article_id": self.id, "slug": self.slug}
        )

    def get_absolute_delete_url(self):
        return reverse(
            "news:delete_article",
            kwargs={"article_id": self.id, "slug": self.slug},
        )

    def get_absolute_edit_url(self):
        return reverse(
            "news:edit_article",
            kwargs={"article_id": self.id, "slug": self.slug},
        )
    
    def send_push(self):
        subscribers = Profile.objects.filter(news_subscription=True)
        for subscriber in subscribers:
            devices = subscriber.devices.all()
            [
                device.send_notification(
                    "Nyhet!", self.title
                )
                for device in devices
            ] # one-liner for loop

def pre_save_article_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


pre_save.connect(pre_save_article_receiver, sender=Article)
