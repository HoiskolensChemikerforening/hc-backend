import json

from django.shortcuts import render
from .models import Travelletter, Experience, Questions, Images
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ExperienceForm, TravelletterForm, QuestionsForm, ImageFormSet
from django.contrib import messages
from chemie.customprofile.models import SPECIALIZATION, Medal
from chemie.chemie.settings.base import CKEDITOR_CONFIGS
from django.utils import timezone


@login_required()
def index(request):

    launch_date = timezone.make_aware(timezone.datetime(2024, 8, 23, 12, 0, 0)) #yyyy m d
    if not request.user.has_perm("exchangepage.add_travelletter") and timezone.now() < launch_date:
        return redirect('exchangepage:countdown')

    travelletters = Travelletter.objects.all().order_by("country")
    avg_list = ['avg_sun', 'avg_livingExpences', 'avg_availability', 'avg_nature', 'avg_hospitality', 'avg_workLoad']
    sort_by = request.GET.get('sort_by', 'country')
    sort_order = request.GET.get('sort_order', 'desc')

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
               }

    return render(request, "index.html", context)


@login_required()
def cityPageViews(request, city_name):
    travelletters = Travelletter.objects.filter(city=city_name).order_by("user")

    if len(travelletters) == 0: #Prevents entering citypages without cities
        return redirect('exchangepage:index')

    sort_list = ['sun', 'livingExpences', 'availability', 'nature', 'hospitality', 'workLoad']
    sort_order = request.GET.get('sort_order', 'desc')
    sort_by = request.GET.get('sort_by', 'user')

    for item in sort_list:
        if sort_by == item:
            if sort_order == 'desc':
                travelletters = travelletters.order_by(item)
            elif sort_order == 'asc':
                travelletters = travelletters.order_by("-"+item)
            break

    context = {
        "city_name": city_name,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "travelletters": travelletters,
    }
    return render(request, "citypage.html", context)

@permission_required("exchangepage.add_travelletter")
def createTravelletterViews(request):
    if request.method == 'POST':
        travelletterform = TravelletterForm(request.POST)
        if travelletterform.is_valid():
            travelletter = travelletterform.save()


            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt reisebrev er lagt inn!",
                extra_tags="Suksess",
            )
            id = travelletter.id
            return redirect('exchangepage:createimage', pk=id)

    else:
        travelletterform = TravelletterForm()

    context = {
        'travelletterform':travelletterform,
    }
    return render(request, "create.html", context)

@permission_required("exchangepage.add_travelletter")
def createImageViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    id = travelletter.id
    print(request.FILES)
    if request.method == 'POST':
        imageformset = ImageFormSet(files=request.FILES, data=request.POST)

        if imageformset.is_valid():

            for form in imageformset:
                image = form.save(commit=False)
                image.travelletter = travelletter
                image.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Bilder er opprettet!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:createexperience', pk=id)  # Redirect to the desired page after successful editing

    else:
        imageformset = ImageFormSet(queryset=Images.objects.none())


    context = {
        'travelletter':travelletter,
        'imageformset':imageformset
    }
    return render(request, "createimage.html", context)

@permission_required("exchangepage.add_travelletter")
def createExperienceViews(request, pk):
    ck_config = CKEDITOR_CONFIGS['news']
    ck_config = json.dumps(ck_config)
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = travelletter.experiences.all()

    if request.method == 'POST':
        experienceform = ExperienceForm(request.POST)


        if experienceform.is_valid():
            experience = experienceform.save(commit=False)
            experience.travelletter = travelletter
            experience.save()  #links the models

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Reisebrevet er opprettet!",
                extra_tags="Suksess",
            )
            experienceform = ExperienceForm()

    else:
        experienceform = ExperienceForm()

    context = {
        'experienceform': experienceform,
        'experiences': experiences,
        'travelletter': travelletter,
        'ck_config': ck_config
    }
    return render(request, "createexperience.html", context)


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

@permission_required('exchangepage.change_images')
def adminDetailImageViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    images = travelletter.images.all()

    if request.method == 'POST':
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
            return redirect('exchangepage:createexperience', pk=pk)  # Redirect to the desired page after successful editing

    else:
        imageformset = ImageFormSet(queryset=images)

    context = {
        'travelletter':travelletter,
        'imageformset':imageformset
    }
    return render(request, "admindetailimage.html", context)

@permission_required('exchangepage.change_experience')
def adminDetailExperienceViews(request, pk):
    ck_config = CKEDITOR_CONFIGS['news']
    ck_config = json.dumps(ck_config)
    experience = get_object_or_404(Experience, pk=pk)
    travelletter = experience.travelletter

    if request.method == 'POST':
        experienceform = ExperienceForm(request.POST, instance=experience)


        if experienceform.is_valid():

            experience = experienceform.save(commit=False)
            experience.travelletter = travelletter
            experience.save()  #links the models

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Hele reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            return redirect('exchangepage:createexperience', pk=travelletter.id)  # Redirect to the desired page after successful editing

    else:
        experienceform = ExperienceForm(instance=experience)


    context = {
        'experienceform': experienceform,
        'experience': experience,
        'travelletter': travelletter,
        'ck_config':ck_config
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
            return redirect('exchangepage:adminquestion')  # Redirect to the desired page after successful editing

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

@permission_required('exchangepage.delete_travelletter')
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

@permission_required('exchangepage.delete_experience')
def deleteExperienceViews(request, pk):
    experience = Experience.objects.get(pk=pk)
    travelletter = experience.travelletter
    experience.delete()

    messages.add_message(
        request,
        messages.WARNING,
        f"Spørsmål slettet!",
        extra_tags="Slettet",
    )
    return redirect('exchangepage:createexperience', pk=travelletter.id)

@permission_required('exchangepage.delete_images')
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
    return redirect('exchangepage:admindetailimage', travelletter.id)

@login_required()
def displayIndividualLetter(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = Experience.objects.filter(travelletter=travelletter)
    questions = [experience.question for experience in experiences]
    images = Images.objects.filter(travelletter=travelletter)

    if len(images) == 0: #QUICKFIIIXX
        images = 0

    else:
        for image in images: #checking if image exists, quickfix
            try:
                image.image.url
            except:
                images=0

    specialization_id = travelletter.user.specialization-1


    context = {'travelletter': travelletter,
               'experiences': experiences,
               'questions': questions,
               'images':images,
               'specialization_id': specialization_id,
               'specialization': SPECIALIZATION[specialization_id][1]
    }

    return render(request, "detail.html", context)

@login_required()
def countDownViews(request):
    #Medals
    webkom = Medal.objects.filter(title="Webkomiteen")
    indkom = Medal.objects.filter(title="Industrikomiteen")
    if len(webkom)>0 and len(indkom)>0:
        webkom = webkom[0]
        indkom = indkom[0]
    else:
        webkom = None
        indkom = None
    context = {'webkom': webkom, 'indkom': indkom}
    return render(request, "countdown.html", context)
