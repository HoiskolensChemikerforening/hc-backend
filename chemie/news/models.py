from django.db import models

# Create your models here.

class NewsPost(models.Model):
    """docstring for NewsPost"""
    published_date=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=120)
    content=models.TextField()
    #author
