from django.db import models
from django.contrib.auth.models import User
  

class Noun(models.Model):
    indefinite_singular = models.CharField(max_length = 100, verbose_name = "ubestemt_entall", unique = True)
    indefinite_plural = models.CharField(max_length = 100, verbose_name = "ubestemt_flertall", unique = True)
    definite_singular = models.CharField(max_length = 100, verbose_name = "bestemt_entall", unique = True)
    definite_plural = models.CharField(max_length = 100, verbose_name = "bestemt_flertall", unique = True)
    
    def __str__(self):
         return self.indefinite_singular

class Verb(models.Model):
    infinitive = models.CharField(max_length = 100, verbose_name = "infinitiv", unique = True)
    present = models.CharField(max_length = 100, verbose_name = "presens", unique = True)
    past = models.CharField(max_length = 100, verbose_name = "preteritum", unique = True)
    future = models.CharField(max_length = 100, verbose_name = "presens futurum", unique = True)

    def __str__(self):
         return self.infinitive


class Adjective(models.Model):
    positive = models.CharField(max_length = 100, verbose_name = "positiv", unique = True)
    comparative = models.CharField(max_length = 100, verbose_name = "komparativ", unique = True)
    superlative = models.CharField(max_length = 100, verbose_name = "superlativ", unique = True)

    def __str__(self):
         return self.positive


class Category(models.Model): 
    typeOfWord = models.CharField(max_length = 100, verbose_name = "Type ord", unique = True)
    
    def __str__(self):
        return self.typeOfWord
    

class Word(models.Model):
    word = models.CharField(max_length = 100, verbose_name = "Ord", unique = True)
    explanations = models.CharField(max_length = 150, verbose_name ="Forklaring",  unique = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Forfatter")
    date = models.DateField(auto_now = False, verbose_name="Dato",auto_now_add=True)
    picture = models.ImageField(upload_to = "posters", verbose_name="Bilde", null = True, blank = True)
    secret = models.BooleanField(default=False, verbose_name="Hemmelig?")
    category = models.ManyToManyField(Category, verbose_name="Kategori", blank=True)
    noun = models.ForeignKey(Noun, on_delete = models.CASCADE, blank=True, null = True, related_name='noun')
    verb = models.ForeignKey(Verb, on_delete = models.CASCADE, blank=True, null = True, related_name='verb')
    adjective = models.ForeignKey(Adjective, on_delete = models.CASCADE, blank=True, null = True, related_name='adjective')

    def __str__(self):
        return self.word
    
    
 



