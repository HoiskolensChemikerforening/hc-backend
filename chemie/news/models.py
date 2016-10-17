from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from sorl.thumbnail import ImageField
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField



class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    content = RichTextField(verbose_name='Beskrivelse', config_name='news_events')
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='news', verbose_name="Bilde")
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={"article_id": self.id, 'slug':self.slug})


def pre_save_article_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


pre_save.connect(pre_save_article_receiver, sender=Article)
