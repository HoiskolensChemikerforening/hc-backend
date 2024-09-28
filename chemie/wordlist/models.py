from django.db import models
from django.contrib.auth.models import User
  

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
    
    def __str__(self):
        return self.word
    

class Noun(Word):
    word = models.CharField(max_length = 100, verbose_name = "ubestemt_entall", unique = False)
    indefinite_plural = models.CharField(max_length = 100, verbose_name = "ubestemt_flertall", unique = False)
    definite_singular = models.CharField(max_length = 100, verbose_name = "bestemt_entall", unique = False)
    definite_plural = models.CharField(max_length = 100, verbose_name = "bestemt_flertall", unique = False)
    
    def __str__(self):
         return self.word

class Verb(Word):
    word = models.CharField(max_length = 100, verbose_name = "infinitiv", unique = False)
    present = models.CharField(max_length = 100, verbose_name = "presens", unique = False)
    past = models.CharField(max_length = 100, verbose_name = "preteritum", unique = False)
    future = models.CharField(max_length = 100, verbose_name = "presens futurum", unique = False)

    def __str__(self):
         return self.word


class Adjective(Word):
    word = models.CharField(max_length = 100, verbose_name = "positiv", unique = False)
    comparative = models.CharField(max_length = 100, verbose_name = "komparativ", unique = False)
    superlative = models.CharField(max_length = 100, verbose_name = "superlativ", unique = False)

    def __str__(self):
         return self.word


    
 



