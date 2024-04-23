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
    
    
 

class Noun(models.Model):
    word = models.ForeignKey(Word, on_delete = models.CASCADE, related_name='noun')
    indefinite_singular = models.CharField(max_length = 100, verbose_name = "ubestemt_entall", unique = True)
    indefinite_plural = models.CharField(max_length = 100, verbose_name = "bestemt_flertall", unique = True)
    definite_singular = models.CharField(max_length = 100, verbose_name = "ubestemt_entall", unique = True)
    definite_plural = models.CharField(max_length = 100, verbose_name = "bestemt_flertall", unique = True)
    
    def __str__(self):
        return self.word


class Verb(models.Model):
    word = models.ForeignKey(Word, on_delete = models.CASCADE, related_name='verb')
    present = models.CharField(max_length = 100, verbose_name = "nåtid", unique = True)
    past = models.CharField(max_length = 100, verbose_name = "fortid", unique = True)
    future = models.CharField(max_length = 100, verbose_name = "fremtid", unique = True)

    def __str__(self):
        return self.word
    


class Adjective(models.Model):
    word = models.ForeignKey(Word, on_delete = models.CASCADE, related_name='adjective')
    positive = models.CharField(max_length = 100, verbose_name = "positiv", unique = True)
    comparative = models.CharField(max_length = 100, verbose_name = "komparativ", unique = True)
    superlative = models.CharField(max_length = 100, verbose_name = "superlativ", unique = True)

    def __str__(self):
        return self.word




# word.noun.prese