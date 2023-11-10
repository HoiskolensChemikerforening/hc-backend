from django.db import models
from chemie.customprofile.models import Profile

class Travelletter(models.Model):
    user           = models.ForeignKey(Profile, on_delete=models.CASCADE)
    country        = models.CharField(max_length=30)
    city           = models.CharField(max_length=30)
    sun            = models.IntegerField(default=0, verbose_name="Score, std1")
    livingExpences = models.IntegerField(default=0, verbose_name="Score, std2")
    availability   = models.IntegerField(default=0, verbose_name="Score, std3")
    nature         = models.IntegerField(default=0, verbose_name="Score, std4")
    hospitality    = models.IntegerField(default=0, verbose_name="Score, std5")
    workLoad       = models.IntegerField(default=0, verbose_name="Score, std6")
    def __str__(self):
        return self.user.user.first_name

class Questions(models.Model):
    question = models.CharField(max_length=200)
    def __str__(self):
        return self.question

class Experience(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.TextField()
    travelletter = models.ForeignKey(Travelletter, on_delete=models.CASCADE, related_name="experiences")
    def __str__(self):
        return f'Svar på spørsmål: {self.question}'





