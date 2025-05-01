from django.db import models
from extended_choices import Choices
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField

ALLERGIES = Choices(
    ("NONE", 1, "Ingen"),
    ("SECOND", 2, "Gluten"),
    ("THIRD", 3, "Peanøtt"),
    ("FOURTH", 4, "Valnøtt"),
    ("FIFTH", 5, "Andre nøtter"),
    ("SIXTH", 6, "Melk/Laktose"),
    ("SEVENTH", 7, "Skalldyr"),
    ("EIGHT", 8, "Soya"),
    ("NINE", 9, "Egg"),
)

KATEGORIER = Choices(
    ("NONE", 1, "Ingen"),
    ("TO", 2, "Dessert"),
    ("TRE", 3, "Kjøtt"),
    ("FIRE", 4, "Vegansk"),
    ("FEM", 5, "Fisk & Skalldyr"),
    ("SEKS", 6, "Pasta & Ris"),
    ("SJU", 7, "Suppe"),
    ("ATTE", 8, "Salater"),
     ("NI", 9, "Vegetar"),
)

def get_defaul_category():
    return [1]

def get_verbose_allergy():
    return "Allergier"

def get_verbose_categories():
    return "Kategorier"

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
    ingredients = RichTextField(
        verbose_name="Ingredienser (X enhet ingrediens, eks 3 ts pepper)", config_name="exchangepage"
    )
    ingredient_quantity = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Antall & Enhet til Ingrediens",
        default=""  # Tom streng som standardverdi
    )
    categories = ArrayField(
        models.PositiveSmallIntegerField(choices=KATEGORIER),
        verbose_name= get_verbose_categories,
        default=get_defaul_category  # Setter en tom liste som standardverdi
    )
    image = ImageField(
        upload_to="matlab",
        verbose_name="Bilde",
        blank=True,
        null=True  # Tillater at bildet ikke er påkrevd
    )
    allowed_allergies = ArrayField(
        models.PositiveSmallIntegerField(choices=ALLERGIES),
        verbose_name=get_verbose_allergy,
        default=get_defaul_category # Setter en tom liste som standardverdi
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
        blank=True,
        default=None
    )

    def __str__(self):
        return f"{self.title}"