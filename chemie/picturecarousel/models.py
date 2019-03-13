from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField
from random import shuffle


class ContributionManager(models.Manager):
    def get_all_shuffled(self):
        result = list(self.filter(approved=True))
        shuffle(result)
        return result


class PictureTag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Contribution(models.Model):
    image = ImageField(upload_to="kontorbilder")
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(PictureTag, blank=True)

    objects = ContributionManager()

    def approve(self):
        self.approved = True
        return True
