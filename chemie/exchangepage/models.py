from django.db import models
from chemie.customprofile.models import Profile

class Travelletter(models.Model):
    user           = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Bruker")
    country        = models.CharField(max_length=30, verbose_name="Land")
    city           = models.CharField(max_length=30, verbose_name="By")
    sun            = models.IntegerField(default=0, verbose_name="Solfaktor")
    livingExpences = models.IntegerField(default=0, verbose_name="Levekostnader")
    availability   = models.IntegerField(default=0, verbose_name="Tilgjengelighet")
    nature         = models.IntegerField(default=0, verbose_name="Natur")
    hospitality   = models.IntegerField(default=0, verbose_name="Gjestfrihet")
    workLoad       = models.IntegerField(default=0, verbose_name="Arbeidsmengde")
    destinationInfo = models.TextField(max_length = 2000, verbose_name="Fakta om land")

    def __str__(self):
        return f"{self.user.user.first_name} {self.country}"

    @classmethod
    def country_avg(cls, country_name):
        travelletters_by_country = cls.objects.filter(country = country_name)

        data = {
            'avg_sun': 0,
            'avg_livingExpences': 0,
            'avg_availability': 0,
            'avg_nature': 0,
            'avg_hospitaility': 0,
            'avg_workLoad': 0,
        }

        for letter in travelletters_by_country:
            data['avg_sun'] += letter.sun
            data['avg_livingExpences'] += letter.livingExpences
            data['avg_availability'] += letter.availability
            data['avg_nature'] += letter.nature
            data['avg_hospitaility'] += letter.hospitality
            data['avg_workLoad'] += letter.workLoad

        data['avg_sun']            /= len(travelletters_by_country)
        data['avg_livingExpences'] /= len(travelletters_by_country)
        data['avg_availability']   /= len(travelletters_by_country)
        data['avg_nature']         /= len(travelletters_by_country)
        data['avg_hospitaility']   /= len(travelletters_by_country)
        data['avg_workLoad']       /= len(travelletters_by_country)

        return data

    @classmethod
    def city_avg(cls, city_name):
        travelletters_by_city = cls.objects.filter(city=city_name)
        country = travelletters_by_city[0].country
        data = {
            'avg_sun': 0,
            'avg_livingExpences': 0,
            'avg_availability': 0,
            'avg_nature': 0,
            'avg_hospitaility': 0,
            'avg_workLoad': 0,
        }

        for letter in travelletters_by_city:
            data['avg_sun'] += letter.sun
            data['avg_livingExpences'] += letter.livingExpences
            data['avg_availability'] += letter.availability
            data['avg_nature'] += letter.nature
            data['avg_hospitaility'] += letter.hospitality
            data['avg_workLoad'] += letter.workLoad

        data['avg_sun']            /= len(travelletters_by_city)
        data['avg_livingExpences'] /= len(travelletters_by_city)
        data['avg_availability']   /= len(travelletters_by_city)
        data['avg_nature']         /= len(travelletters_by_city)
        data['avg_hospitaility']   /= len(travelletters_by_city)
        data['avg_workLoad']       /= len(travelletters_by_city)

        return country, data


class Questions(models.Model):
    question = models.CharField(max_length=200, verbose_name="Spørsmål")
    def __str__(self):
        return self.question

class Experience(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="Spørsmål")
    answer = models.TextField(verbose_name="Svar")
    travelletter = models.ForeignKey(Travelletter, on_delete=models.CASCADE, related_name="experiences")
    def __str__(self):
        return f'Svar på spørsmål: {self.question}'

class Images(models.Model):
    travelletter = models.ForeignKey(Travelletter, on_delete=models.CASCADE, related_name='images', verbose_name="Reisebrev")
    image = models.ImageField(upload_to="exchangepage", verbose_name="Bilde")

    def __str__(self):
        return f'Bilde id: {self.id}, Reisebrev: {self.travelletter}'





