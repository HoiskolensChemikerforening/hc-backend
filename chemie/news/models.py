from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify



class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(null=True, blank=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={"event_id": self.id})


    #def get_absolute_registration_url(self):
    #    return reverse('events:register', kwargs={"event_id": self.id})