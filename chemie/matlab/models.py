from django.db import models
from extended_choices import Choices
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

ALLERGIES = Choices(
    ("FIRST", 1, "Egg"),
    ("SECOND", 2, "Gluten"),
    ("THIRD", 3, "Peanøtt"),
    ("FOURTH", 4, "Valnøtt"),
    ("FIFTH", 5, "Andre nøtter"),
    ("SIXTH", 6, "Melk/Laktose"),
    ("SEVENTH", 7, "Skalldyr"),
    ("EIGHT", 8, "Soya"),
)

KATEGORIER = Choices(
    ("FIRST", 1, "Vegetar"),
    ("SECOND", 2, "Dessert"),
    ("THIRD", 3, "Kjøtt"),
    ("FOURTH", 4, "Vegansk"),
    ("FIFTH", 5, "Fisk & Skalldyr"),
    ("SIXTH", 6, "Pasta & Ris"),
    ("SEVENTH", 7, "Suppe"),
    ("EIGHT", 8, "Salater"),
)

class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    #quantity = models.PositiveSmallIntegerField() #1kg løk og 1stk løk vil være to ingredienser... løk er jo løk
    #unit = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Recipes(models.Model):
    title = models.CharField(
        verbose_name="Navn på rett",
        max_length=30,
        default=""  # Tom streng som standardverdi
    )
    time = models.PositiveSmallIntegerField(
        verbose_name="Tid [min] ",
        default=0  # Standard tid til 0 minutter
    )
    description = models.TextField(
        verbose_name="Fremgangmåte",
        blank=True,
        default=""  # Tom streng som standardverdi
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        blank=True,
        verbose_name="Ingredienser",
    )
    ingredient_quantity = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Antall & Enhet til Ingrediens",
        default=""  # Tom streng som standardverdi
    )
    categories = ArrayField(
        models.CharField(choices=KATEGORIER, max_length=100),
        verbose_name="Kategorier",
        default=list  # Setter en tom liste som standardverdi
    )
    image = ImageField(
        upload_to="matlab",
        verbose_name="Bilde",
        blank=True,
        null=True  # Tillater at bildet ikke er påkrevd
    )
    allowed_allergies = ArrayField(
        models.CharField(choices=ALLERGIES, max_length=100),
        verbose_name="Allergier",
        default=list  # Setter en tom liste som standardverdi
    )
    expected_price = models.PositiveSmallIntegerField(
        verbose_name="Antatt pris",
        default=0  # Setter pris til 0 som standard
    )
    portions = models.PositiveSmallIntegerField(
        verbose_name="Antall Porsjoner beregnet for",
        default=1  # Setter standard porsjonsantall til 1
    )
    author = models.ForeignKey(
        User,
        related_name="recipes_author",
        on_delete=models.CASCADE,
        default=""
    )

    def __str__(self):
        return f"{self.title}"