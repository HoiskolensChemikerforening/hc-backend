from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=30)
    authour = models.CharField(max_length=30)
    COLORS = {
        "Red","Blue","Brown","Black"
    }
    color = models.CharField(max_length=1,choices=COLORS)

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    Date_of_birth = models.DateTimeField

class Genres(models.Model):
    name = models.CharField(max_length=50)