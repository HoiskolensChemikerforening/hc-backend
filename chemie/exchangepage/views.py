from django.shortcuts import render
from .models import Travelletter, Experience, Questions
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required()
def index(request):
    travelletters = Travelletter.objects.all().order_by("country")

    # Group the travelletters by country
    travelletters_by_country = {}
    for letter in travelletters:
        country = letter.country
        if country not in travelletters_by_country:
            travelletters_by_country[country] = {
                'count': 0,
                'avg_sun': 0,
                'avg_livingExpences': 0,
                'avg_availability': 0,
                'avg_nature': 0,
                'avg_hospitality': 0,
                'avg_workLoad': 0,
            }
        travelletters_by_country[country]['count'] += 1
        travelletters_by_country[country]['avg_sun'] += letter.sun
        travelletters_by_country[country]['avg_livingExpences'] += letter.livingExpences
        travelletters_by_country[country]['avg_availability'] += letter.availability
        travelletters_by_country[country]['avg_nature'] += letter.nature
        travelletters_by_country[country]['avg_hospitality'] += letter.hospitality
        travelletters_by_country[country]['avg_workLoad'] += letter.workLoad

    # Calculate the average values for each country
    for country, data in travelletters_by_country.items():
        count = data['count']
        data['avg_sun'] /= count
        data['avg_livingExpences'] /= count
        data['avg_availability'] /= count
        data['avg_nature'] /= count
        data['avg_hospitality'] /= count
        data['avg_workLoad'] /= count


    data_by_country_city = {}
    for letter in travelletters:
        country = letter.country
        city = letter.city

        if country not in data_by_country_city:
            data_by_country_city[country] = {}
        if city not in data_by_country_city[country]:
            data_by_country_city[country][city] = {
                'count': 0,
                'avg_sun': 0,
                'avg_livingExpences': 0,
                'avg_availability': 0,
                'avg_nature': 0,
                'avg_hospitality': 0,
                'avg_workLoad': 0,
            }

        data_by_country_city[country][city]['count'] += 1
        data_by_country_city[country][city]['avg_sun'] += letter.sun
        data_by_country_city[country][city]['avg_livingExpences'] += letter.livingExpences
        data_by_country_city[country][city]['avg_availability'] += letter.availability
        data_by_country_city[country][city]['avg_nature'] += letter.nature
        data_by_country_city[country][city]['avg_hospitality'] += letter.hospitality
        data_by_country_city[country][city]['avg_workLoad'] += letter.workLoad

    # Calculate the average values for each city within each country
    for country, cities in data_by_country_city.items():
        for city, data in cities.items():
            count = data['count']
            data['avg_sun'] /= count
            data['avg_livingExpences'] /= count
            data['avg_availability'] /= count
            data['avg_nature'] /= count
            data['avg_hospitality'] /= count
            data['avg_workLoad'] /= count
    print(travelletters_by_country)
    print(data_by_country_city)
    context = {"travelletters_by_country": travelletters_by_country, "data_by_city": data_by_country_city}
    return render(request, "index.html", context)

@login_required()
def cityPageViews(request, city_name):
    context = {"city_name":city_name}
    return render(request, "citypage.html", context)

@login_required()
def detailViews(request, pk):
    context = {}
    return render(request, "detail.html", context)

@permission_required("exchangepage.add_travelletter")
def createViews(request):
    return render(request, "create.html")

@permission_required("exchangepage.change_travelletter")
def adminViews(request):
    return render(request, "admin.html")



