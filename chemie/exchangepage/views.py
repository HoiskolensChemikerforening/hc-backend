from django.shortcuts import render
from .models import Travelletter, Experience, Questions
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import IndexForm, ExperienceForm, TravelletterForm, QuestionsForm
from django.contrib import messages


# Create your views here.

@login_required()
def index(request):
    travelletters = Travelletter.objects.all().order_by("country")
    avg_list = ['avg_sun', 'avg_livingExpences', 'avg_availability', 'avg_nature', 'avg_hospitality', 'avg_workLoad']
    sort_by = request.GET.get('sort_by', 'country')
    sort_order = request.GET.get('sort_order', 'desc')

    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data
            # print(form)
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
        data_by_country_city[country][city] = data

    reverse_order = sort_order == 'desc'
    for avg in avg_list:
        if sort_by == avg:
            travelletters_by_country = dict(
                sorted(travelletters_by_country.items(), key=lambda x: x[1][avg], reverse=reverse_order))
            for country, city_data in data_by_country_city.items():
                data_by_country_city[country] = dict(
                    sorted(city_data.items(), key=lambda x: x[1][avg], reverse=reverse_order))

            break

    context = {"travelletters_by_country": travelletters_by_country,
               "data_by_city": data_by_country_city,
               "sort_by": sort_by,
               "sort_order": sort_order,
               "form": form}

    return render(request, "index.html", context)


@login_required()
def cityPageViews(request, city_name):
    travelletters = Travelletter.objects.filter(city=city_name).order_by("user")
    context = {
        "city_name": city_name,
        "travelletters": travelletters,
    }
    return render(request, "citypage.html", context)


@login_required()
def detailViews(request, pk):
    travelletter = Travelletter.objects.get(id=pk)

    print(travelletter.user)

    context = {
        'travelletter': travelletter,
    }

    return render(request, "detail.html", context)


@permission_required("exchangepage.add_travelletter")
def createViews(request):
    if request.method == 'POST':
        travelletterform = TravelletterForm(request.POST)
        experienceform = ExperienceForm(request.POST)
        questionform = QuestionsForm(request.POST)
        if experienceform.is_valid() and travelletterform.is_valid() and questionform.is_valid():
            travelletter = travelletterform.save()
            question = questionform.save()
            experience = experienceform.save(commit=False)
            experience.travelletter = travelletter
            experience.question = question
            experience.save()  # links the models

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt reisebrev er lagt inn!",
                extra_tags="Suksess",
            )
            travelletterform = TravelletterForm()  # show empty forms after completed
            experienceform = ExperienceForm()
            questionform = QuestionsForm()

    else:
        travelletterform = TravelletterForm()
        experienceform = ExperienceForm()
        questionform = QuestionsForm()

    context = {
        'experienceform': experienceform,
        'travelletterform': travelletterform,
        'questionform': questionform
    }
    return render(request, "create.html", context)


@permission_required("exchangepage.change_travelletter")
def adminViews(request):
    experiences = Experience.objects.all().order_by("id")
    context = {'experiences': experiences}
    return render(request, "admin.html", context)


@permission_required("exchangepage.change_travelletter")
def adminDetailViews(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    travelletter = experience.travelletter
    question = experience.question

    if request.method == 'POST':
        travelletterform = TravelletterForm(request.POST, instance=travelletter)
        experienceform = ExperienceForm(request.POST, instance=experience)
        questionform = QuestionsForm(request.POST, instance=question)

        if experienceform.is_valid() and travelletterform.is_valid() and questionform.is_valid():
            travelletterform.save()
            questionform.save()
            experienceform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:admin')  # Redirect to the desired page after successful editing

    else:
        travelletterform = TravelletterForm(instance=travelletter)
        experienceform = ExperienceForm(instance=experience)
        questionform = QuestionsForm(instance=question)

    context = {
        'experienceform': experienceform,
        'travelletterform': travelletterform,
        'questionform': questionform
    }
    return render(request, "admindetail.html", context)


def displayIndividualLetter(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = Experience.objects.filter(travelletter=travelletter)
    questions = [experience.question for experience in experiences]

    print("Experiences length:", len(experiences))
    print("Questions length:", len(questions))
    print("Experiences:", experiences)

    context = {'travelletter': travelletter,
               'experiences': experiences,
               'questions': questions
    }

    print(len(experiences))

    return render(request, "detail.html", context)

