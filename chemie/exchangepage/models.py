from django.db import models
from chemie.customprofile.models import Profile
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from ckeditor.fields import RichTextField


class Travelletter(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Bruker"
    )
    country = models.CharField(max_length=30, verbose_name="Land")
    semester = models.CharField(
        max_length=7,
        validators=[MinLengthValidator(3), MaxLengthValidator(7)],
        verbose_name="Semester",
    )
    city = models.CharField(max_length=30, verbose_name="By")
    sun = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Solfaktor",
    )
    livingExpences = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Levekostnader",
    )
    availability = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Tilgjengelighet",
    )
    nature = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Natur",
    )
    hospitality = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Gjestfrihet",
    )
    workLoad = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Arbeidsmengde",
    )
    destinationInfo = RichTextField(
        max_length=700, verbose_name="Info om sted", config_name="exchangepage"
    )

    def __str__(self):
        return f"{self.user.user.first_name} {self.country}"

    def save(self, *args, **kwargs):
        """Make the first letter uppercase for country and city"""
        if self.country:
            self.country = self.country[0].upper() + self.country[1:]
        if self.city:
            self.city = self.city[0].upper() + self.city[1:]

        super(Travelletter, self).save(*args, **kwargs)

    @classmethod
    def country_avg(cls, country_name):
        """Calculate the average values for each country"""
        travelletters_by_country = cls.objects.filter(country=country_name)

        data = {
            "avg_sun": 0,
            "avg_livingExpences": 0,
            "avg_availability": 0,
            "avg_nature": 0,
            "avg_hospitality": 0,
            "avg_workLoad": 0,
        }

        for letter in travelletters_by_country:
            data["avg_sun"] += letter.sun
            data["avg_livingExpences"] += letter.livingExpences
            data["avg_availability"] += letter.availability
            data["avg_nature"] += letter.nature
            data["avg_hospitality"] += letter.hospitality
            data["avg_workLoad"] += letter.workLoad

        num_letters = len(travelletters_by_country)
        data["avg_sun"] = round(data["avg_sun"] / num_letters, 1)
        data["avg_livingExpences"] = round(
            data["avg_livingExpences"] / num_letters, 1
        )
        data["avg_availability"] = round(
            data["avg_availability"] / num_letters, 1
        )
        data["avg_nature"] = round(data["avg_nature"] / num_letters, 1)
        data["avg_hospitality"] = round(
            data["avg_hospitality"] / num_letters, 1
        )
        data["avg_workLoad"] = round(data["avg_workLoad"] / num_letters, 1)

        return data

    @classmethod
    def city_avg(cls, city_name):
        """Calculate the average values for each city"""
        travelletters_by_city = cls.objects.filter(city=city_name)
        country = travelletters_by_city[0].country
        data = {
            "avg_sun": 0,
            "avg_livingExpences": 0,
            "avg_availability": 0,
            "avg_nature": 0,
            "avg_hospitality": 0,
            "avg_workLoad": 0,
        }

        for letter in travelletters_by_city:
            data["avg_sun"] += letter.sun
            data["avg_livingExpences"] += letter.livingExpences
            data["avg_availability"] += letter.availability
            data["avg_nature"] += letter.nature
            data["avg_hospitality"] += letter.hospitality
            data["avg_workLoad"] += letter.workLoad

        num_letters = len(travelletters_by_city)
        data["avg_sun"] = round(data["avg_sun"] / num_letters, 1)
        data["avg_livingExpences"] = round(
            data["avg_livingExpences"] / num_letters, 1
        )
        data["avg_availability"] = round(
            data["avg_availability"] / num_letters, 1
        )
        data["avg_nature"] = round(data["avg_nature"] / num_letters, 1)
        data["avg_hospitality"] = round(
            data["avg_hospitality"] / num_letters, 1
        )
        data["avg_workLoad"] = round(data["avg_workLoad"] / num_letters, 1)

        return country, data


class Questions(models.Model):
    question = models.CharField(max_length=200, verbose_name="Spørsmål")

    def __str__(self):
        return self.question


class Experience(models.Model):
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, verbose_name="Spørsmål"
    )
    answer = RichTextField(verbose_name="Svar", config_name="exchangepage")
    travelletter = models.ForeignKey(
        Travelletter, on_delete=models.CASCADE, related_name="experiences"
    )

    def __str__(self):
        return f"Svar på spørsmål: {self.question}"


class Images(models.Model):
    travelletter = models.ForeignKey(
        Travelletter,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Reisebrev",
    )
    image = models.ImageField(
        upload_to="exchangepage", verbose_name="Bilde", blank=False
    )

    def __str__(self):
        return f"Bilde id: {self.id}, Reisebrev: {self.travelletter}"
