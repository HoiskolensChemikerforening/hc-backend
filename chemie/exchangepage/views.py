from django.shortcuts import render
from .models import Travelletter, Experience, Questions
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required()
def index(request):
    travelletters = Travelletter.objects.all().order_by("country")

    # Group the travelletters by country
    travelletters_by_country = {}
    data_by_country_city = {}
    country_list = []
    city_list = []

    for letter in travelletters:
        country = letter.country
        city = letter.city
        if country not in country_list:
            country_list.append(country)

        if city not in city_list:
            city_list.append(city)

        if country not in data_by_country_city:
            data_by_country_city[country] = {}

    for country in country_list:
        travelletters_by_country[country] = Travelletter.country_avg(country)

    for city in city_list:
        country, data = Travelletter.city_avg(city)
        data_by_country_city[country][city]= data



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



