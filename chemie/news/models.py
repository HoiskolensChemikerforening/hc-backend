from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(null=True, blank=True)
    #author

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
