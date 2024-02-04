from django.shortcuts import render
from .models import Travelletter, Experience, Questions, Images
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import IndexForm, ExperienceForm, TravelletterForm, QuestionsForm, ExperienceFormSet, ImageFormSet, ImageForm
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
        print(request.POST)
        print("hei", request.POST['form-TOTAL_FORMS'])
        travelletterform = TravelletterForm(request.POST)
        experienceformset = ExperienceFormSet(request.POST)
        imageformset = ImageFormSet(files=request.FILES, data=request.POST)
        if experienceformset.is_valid() and travelletterform.is_valid() and imageformset.is_valid():
            travelletter = travelletterform.save()

            for form in experienceformset:
                experience = form.save(commit=False)
                experience.travelletter = travelletter
                experience.save()  #links the models

            for form in imageformset:
                image = form.save(commit = False)
                image.travelletter = travelletter
                image.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt reisebrev er lagt inn!",
                extra_tags="Suksess",
            )

            return redirect('exchangepage:admin')

    else:
        travelletterform = TravelletterForm()
        experienceformset = ExperienceFormSet(queryset=Experience.objects.none())
        imageformset = ImageFormSet(queryset=Images.objects.none())

    context = {
        'experienceformset':experienceformset,
        'travelletterform':travelletterform,
        'imageformset':imageformset
    }
    return render(request, "create.html", context)


@permission_required("exchangepage.change_travelletter")
def adminViews(request):
    travelletters = Travelletter.objects.all().order_by("id")
    context = {'travelletters':travelletters}
    return render(request, "admin.html", context)


@permission_required("exchangepage.change_travelletter")
def adminDetailViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)

    if request.method == 'POST':
        travelletterform = TravelletterForm(request.POST, instance=travelletter)

        if travelletterform.is_valid():
            travelletterform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:admindetailimage',pk=pk)  # Redirect to the desired page after successful editing

    else:
        travelletterform = TravelletterForm(instance=travelletter)

    context = {
        'travelletterform': travelletterform,
        'travelletter':travelletter,
    }
    return render(request, "admindetail.html", context)

def adminDetailImageViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    images = travelletter.images.all()

    if request.method == 'POST':
        print(request.FILES)
        imageformset = ImageFormSet(files=request.FILES, data=request.POST, queryset=images)

        if imageformset.is_valid():

            for form in imageformset:
                image = form.save(commit=False)
                image.travelletter = travelletter
                image.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Bilder er oppdatert!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:admindetailexperience', pk=pk)  # Redirect to the desired page after successful editing

    else:
        imageformset = ImageFormSet(queryset=images)

    context = {
        'travelletter':travelletter,
        'imageformset':imageformset
    }
    return render(request, "admindetailimage.html", context)

def adminDetailExperienceViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = travelletter.experiences.all()

    if request.method == 'POST':
        experienceformset = ExperienceFormSet(request.POST, queryset=experiences)


        if experienceformset.is_valid():
            for form in experienceformset:
                experience = form.save(commit=False)
                experience.travelletter = travelletter
                experience.save()  #links the models

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Hele reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:admin')  # Redirect to the desired page after successful editing

    else:
        experienceformset = ExperienceFormSet(queryset=experiences)


    context = {
        'experienceformset': experienceformset,
        'travelletter': travelletter
    }
    return render(request, "admindetailexperience.html", context)

@permission_required("exchangepage.change_travelletter")
def createQuestionViews(request):
    if request.method == 'POST':
        questionform = QuestionsForm(request.POST)
        if questionform.is_valid():
            questionform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt spørsmål opprettet!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:index')  # Redirect to the desired page after successful editing

    else:
        questionform = QuestionsForm()

    context = {'questionform':questionform}
    return render(request, "createquestion.html", context)

@permission_required("exchangepage.change_travelletter")
def adminQuestionViews(request):
    questions = Questions.objects.all().order_by("id")
    context = {'questions':questions}
    return render(request, "adminquestion.html", context)

@permission_required("exchangepage.change_travelletter")
def adminQuestionDetailViews(request, pk):
    question = get_object_or_404(Questions, pk=pk)

    if request.method == 'POST':
        questionform = QuestionsForm(request.POST, instance=question)
        if questionform.is_valid():
            questionform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Spørsmålet er endret!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:adminquestion')  # Redirect to the desired page after successful editing

    else:
        questionform = QuestionsForm(instance=question)
        print(questionform)

    context = {'questionform':questionform}
    return render(request, "adminquestiondetail.html", context)

def deleteTravelletter(request, pk):
    query = Travelletter.objects.get(pk=pk)
    query.delete()

    messages.add_message(
        request,
        messages.WARNING,
        f"Reisebrev slettet!",
        extra_tags="Slettet",
    )
    return redirect('exchangepage:admin')

def deleteImages(request, pk):
    travelletter = Travelletter.objects.get(pk=pk)
    images = travelletter.images.all()
    images.delete()

    messages.add_message(
        request,
        messages.WARNING,
        f"Bilder slettet!",
        extra_tags="Slettet",
    )
    return redirect('exchangepage:admin')

def displayIndividualLetter(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = Experience.objects.filter(travelletter=travelletter)
    questions = [experience.question for experience in experiences]
    images = travelletter.images.all()

    print("Experiences length:", len(experiences))
    print("Questions length:", len(questions))
    print("Experiences:", experiences)

    context = {'travelletter': travelletter,
               'experiences': experiences,
               'questions': questions,
               'images':images
    }

    print(len(experiences))

    return render(request, "detail.html", context)

