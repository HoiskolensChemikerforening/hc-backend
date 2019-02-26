from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class QuizTerm(models.Model):
    is_active = models.BooleanField()
    term = models.CharField(max_length=100)


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.ForeignKey(QuizTerm, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
