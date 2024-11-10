from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    typeOfWord = models.CharField(
        max_length=100, verbose_name="Type ord", unique=True
    )

    def __str__(self):
        return self.typeOfWord


class AbstractWord(models.Model):
    explanations = models.CharField(
        max_length=300, verbose_name="Forklaring", unique=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Forfatter"
    )
    date = models.DateField(
        auto_now=False, verbose_name="Dato", auto_now_add=True
    )
    picture = models.ImageField(
        upload_to="posters", verbose_name="Bilde", null=True, blank=True
    )
    secret = models.BooleanField(default=False, verbose_name="Hemmelig?")
    category = models.ManyToManyField(
        Category, verbose_name="Kategori", blank=True
    )

    class Meta:  # Viktig for å kunne lage fields i subclasses (Noun, Verb, Adjective, Word) som ikkje skal komme i konflikt med AbstractWord
        abstract = True  # Definerer den som en kun abstract class, fordi det aldri vil eksisterer et objekt i AbstractWord


class Noun(AbstractWord):
    word = models.CharField(
        max_length=100,
        verbose_name="ubestemt_entall",
        unique=False,
        blank=True,
    )
    indefinite_plural = models.CharField(
        max_length=100,
        verbose_name="ubestemt_flertall",
        unique=False,
        blank=True,
    )
    definite_singular = models.CharField(
        max_length=100, verbose_name="bestemt_entall", unique=False, blank=True
    )
    definite_plural = models.CharField(
        max_length=100,
        verbose_name="bestemt_flertall",
        unique=False,
        blank=True,
    )

    def __str__(self):
        return self.word


class Verb(AbstractWord):
    word = models.CharField(
        max_length=100, verbose_name="infinitiv", unique=False, blank=True
    )
    present = models.CharField(
        max_length=100, verbose_name="presens", unique=False, blank=True
    )
    past = models.CharField(
        max_length=100, verbose_name="preteritum", unique=False, blank=True
    )
    future = models.CharField(
        max_length=100,
        verbose_name="presens futurum",
        unique=False,
        blank=True,
    )

    def __str__(self):
        return self.word


class Adjective(AbstractWord):
    word = models.CharField(
        max_length=100, verbose_name="positiv", unique=False, blank=True
    )
    comparative = models.CharField(
        max_length=100, verbose_name="komparativ", unique=False, blank=True
    )
    superlative = models.CharField(
        max_length=100, verbose_name="superlativ", unique=False, blank=True
    )

    def __str__(self):
        return self.word


class Word(AbstractWord):
    word = models.CharField(
        max_length=100, verbose_name="Ord", unique=True, blank=True
    )

    def __str__(self):
        return self.word
