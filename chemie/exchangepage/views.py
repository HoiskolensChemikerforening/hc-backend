from django.shortcuts import render
from .models import Travelletter, Experience, Questions
from itertools import groupby

# Create your views here.

def index(request):
    travelletters = Travelletter.objects.all().order_by("country")

    # Group the travelletters by country
    travelletters_by_country = {}
    for letter in travelletters:
        country = letter.country
        if country not in travelletters_by_country:
            travelletters_by_country[country] = {
                'count': 0,
                'avg_std1': 0,
                'avg_std2': 0,
                'avg_std3': 0,
                'avg_std4': 0,
                'avg_std5': 0,
                'avg_std6': 0,
            }
        travelletters_by_country[country]['count'] += 1
        travelletters_by_country[country]['avg_std1'] += letter.std1
        travelletters_by_country[country]['avg_std2'] += letter.std2
        travelletters_by_country[country]['avg_std3'] += letter.std3
        travelletters_by_country[country]['avg_std4'] += letter.std4
        travelletters_by_country[country]['avg_std5'] += letter.std5
        travelletters_by_country[country]['avg_std6'] += letter.std6

    # Calculate the average values for each country
    for country, data in travelletters_by_country.items():
        count = data['count']
        data['avg_std1'] /= count
        data['avg_std2'] /= count
        data['avg_std3'] /= count
        data['avg_std4'] /= count
        data['avg_std5'] /= count
        data['avg_std6'] /= count


    data_by_country_city = {}
    for letter in travelletters:
        country = letter.country
        city = letter.city

        if country not in data_by_country_city:
            data_by_country_city[country] = {}
        if city not in data_by_country_city[country]:
            data_by_country_city[country][city] = {
                'count': 0,
                'avg_std1': 0,
                'avg_std2': 0,
                'avg_std3': 0,
                'avg_std4': 0,
                'avg_std5': 0,
                'avg_std6': 0,
            }

        data_by_country_city[country][city]['count'] += 1
        data_by_country_city[country][city]['avg_std1'] += letter.std1
        data_by_country_city[country][city]['avg_std2'] += letter.std2
        data_by_country_city[country][city]['avg_std3'] += letter.std3
        data_by_country_city[country][city]['avg_std4'] += letter.std4
        data_by_country_city[country][city]['avg_std5'] += letter.std5
        data_by_country_city[country][city]['avg_std6'] += letter.std6

    # Calculate the average values for each city within each country
    for country, cities in data_by_country_city.items():
        for city, data in cities.items():
            count = data['count']
            data['avg_std1'] /= count
            data['avg_std2'] /= count
            data['avg_std3'] /= count
            data['avg_std4'] /= count
            data['avg_std5'] /= count
            data['avg_std6'] /= count

    context = {"travelletters_by_country": travelletters_by_country, "data_by_city": data_by_country_city}
    return render(request, "index.html", context)

def cityPageViews(request, city_name):
    context = {"city_name":city_name}
    return render(request, "citypage.html", context)

def detailViews(request, pk):
    context = {}
    return render(request, "detail.html", context)

def createViews(request):
    return render(request, "create.html")

def adminViews(request):
    return render(request, "admin.html")



