from django.shortcuts import render
from .models import Travelletter, Experience, Questions
from django.contrib.auth.decorators import login_required, permission_required
from .forms import IndexForm
# Create your views here.

@login_required()
def index(request):
    travelletters = Travelletter.objects.all().order_by("country")
    avg_list = ['avg_sun', 'avg_livingExpences', 'avg_availability','avg_nature', 'avg_hospitality', 'avg_workLoad']
    sort_by = request.GET.get('sort_by', 'country')
    sort_order = request.GET.get('sort_order', 'desc')

    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data['Indexfiltering']
            print("Test", test)
    else:
        form = IndexForm()
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

    reverse_order = sort_order == 'desc'
    for avg in avg_list:
        if sort_by == avg:
            travelletters_by_country = dict(sorted(travelletters_by_country.items(), key=lambda x: x[1][avg],reverse=reverse_order))
            for country, city_data in data_by_country_city.items():
                data_by_country_city[country] = dict(sorted(city_data.items(), key=lambda x: x[1][avg], reverse=reverse_order))

            break

    print(travelletters_by_country)
    print(data_by_country_city)

    context = {"travelletters_by_country": travelletters_by_country,
               "data_by_city": data_by_country_city,
               "sort_by": sort_by,
               "sort_order": sort_order,
               "form": form}

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



