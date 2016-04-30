from django.db import models

# Create your models here.

class NewsPost(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    #author

    def __str__(self):
        return self.title
