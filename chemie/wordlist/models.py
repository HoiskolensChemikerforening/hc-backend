from django.db import models
from django.contrib.auth.models import User



class Word(models.Model):
    word = models.CharField(max_length = 100, unique = True)
    explanations = models.CharField(max_length = 150, unique = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Forfatter")
    date = models.DateField(auto_now = False, auto_now_add= False)
    picture = models.ImageField(upload_to = "posters", null = True, blank = True)
    secret = models.BooleanField(default=False)

    def __str__(self):
        return self.word
    
    
        

class Category(models.Model): 
    typeOfWord = models.CharField(max_length = 100, unique = True)
    Words = models.ManyToManyField(Word, verbose_name="Ord", blank=True)

    def __str__(self):
        return self.typeOfWord
    
