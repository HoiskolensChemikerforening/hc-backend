from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    ingress_content = models.TextField()
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(null=True, blank=True)
    #author

    def __str__(self):
        return self.title
