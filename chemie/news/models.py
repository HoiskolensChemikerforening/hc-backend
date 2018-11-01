from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from sorl.thumbnail import ImageField


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    content = RichTextField(verbose_name='Beskrivelse', config_name='news')
    published_date = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='news', verbose_name="Bilde")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={"article_id": self.id, 'slug':self.slug})


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200, verbose_name='Skriv en kommentar')
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'


    def __str__(self):
        return self.text




def pre_save_article_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


pre_save.connect(pre_save_article_receiver, sender=Article)
