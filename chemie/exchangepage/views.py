from django.shortcuts import render
from .models import Travelletter, Experience, Questions, Images
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import (
    ExperienceForm,
    TravelletterForm,
    QuestionsForm,
    ImageFormSet,
)
from django.contrib import messages
from chemie.customprofile.models import SPECIALIZATION, Medal
from django.utils import timezone


@login_required()
def index(request):
    travelletters = Travelletter.objects.all().order_by("country")
    avg_list = [
        "avg_sun",
        "avg_livingExpences",
        "avg_availability",
        "avg_nature",
        "avg_hospitality",
        "avg_workLoad",
        "alphabetic",
    ]
    sort_by = request.GET.get("sort_by", "country")
    sort_order = request.GET.get("sort_order", "desc")

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

    # Logic for sorting the table
    reverse_order = sort_order == "desc"
    if sort_by == "alphabetic":
        travelletters_by_country = dict(
            sorted(
                travelletters_by_country.items(),
                key=lambda x: x[0],
                reverse=reverse_order,
            )
        )
        for country, city_data in data_by_country_city.items():
            data_by_country_city[country] = dict(
                sorted(
                    city_data.items(),
                    key=lambda x: x[0],
                    reverse=reverse_order,
                )
            )
    else:
        for avg in avg_list:
            if sort_by == avg:
                travelletters_by_country = dict(
                    sorted(
                        travelletters_by_country.items(),
                        key=lambda x: x[1][avg],
                        reverse=reverse_order,
                    )
                )
                for country, city_data in data_by_country_city.items():
                    data_by_country_city[country] = dict(
                        sorted(
                            city_data.items(),
                            key=lambda x: x[1][avg],
                            reverse=reverse_order,
                        )
                    )

                break

    context = {
        "travelletters_by_country": travelletters_by_country,
        "data_by_city": data_by_country_city,
        "sort_by": sort_by,
        "sort_order": sort_order,
    }

    return render(request, "exchangepage/index.html", context)


@login_required()
def cityPageViews(request, city_name):
    travelletters = Travelletter.objects.filter(city=city_name).order_by(
        "user"
    )

    # Prevents entering citypages without cities
    if len(travelletters) == 0:
        return redirect("exchangepage:index")

    sort_list = [
        "sun",
        "livingExpences",
        "availability",
        "nature",
        "hospitality",
        "workLoad",
        "user",
    ]
    sort_order = request.GET.get("sort_order", "desc")
    sort_by = request.GET.get("sort_by", "user")

    # Logic for sorting the table
    for item in sort_list:
        if sort_by == item:
            if sort_order == "desc":
                travelletters = travelletters.order_by(item)
            elif sort_order == "asc":
                travelletters = travelletters.order_by("-" + item)
            break

    context = {
        "city_name": city_name,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "travelletters": travelletters,
    }
    return render(request, "exchangepage/citypage.html", context)


@permission_required("exchangepage.add_travelletter")
def createTravelletterViews(request):
    if request.method == "POST":
        travelletterform = TravelletterForm(request.POST)
        if travelletterform.is_valid():
            travelletter = travelletterform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt reisebrev er lagt inn!",
                extra_tags="Suksess",
            )

            return redirect("exchangepage:createimage", pk=travelletter.id)

    else:
        travelletterform = TravelletterForm()

    context = {
        "travelletterform": travelletterform,
    }
    return render(request, "exchangepage/create.html", context)


@permission_required("exchangepage.add_travelletter")
def createImageViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    if request.method == "POST":
        imageformset = ImageFormSet(files=request.FILES, data=request.POST)

        if imageformset.is_valid():
            for form in imageformset:
                if form.is_valid() and form.cleaned_data.get("image"):
                    image = form.save(commit=False)
                    image.travelletter = travelletter
                    image.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Bilder er opprettet!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect(
                "exchangepage:createexperience", pk=travelletter.id
            )

    else:
        imageformset = ImageFormSet(queryset=Images.objects.none())

    context = {"travelletter": travelletter, "imageformset": imageformset}
    return render(request, "exchangepage/createimage.html", context)


@permission_required("exchangepage.add_travelletter")
def createExperienceViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = travelletter.experiences.all()

    if request.method == "POST":
        experienceform = ExperienceForm(request.POST)

        if experienceform.is_valid():
            experience = experienceform.save(commit=False)
            experience.travelletter = travelletter
            experience.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Reisebrevet er opprettet!",
                extra_tags="Suksess",
            )
            return redirect("exchangepage:createexperience", pk=pk)

    else:
        experienceform = ExperienceForm()

    context = {
        "experienceform": experienceform,
        "experiences": experiences,
        "travelletter": travelletter,
    }
    return render(request, "exchangepage/createexperience.html", context)


@permission_required("exchangepage.change_travelletter")
def adminViews(request):
    travelletters = Travelletter.objects.all().order_by("id")
    context = {"travelletters": travelletters}
    return render(request, "exchangepage/admin.html", context)


@permission_required("exchangepage.change_travelletter")
def adminDetailViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)

    if request.method == "POST":
        travelletterform = TravelletterForm(
            request.POST, instance=travelletter
        )

        if travelletterform.is_valid():
            travelletterform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect("exchangepage:admindetailimage", pk=pk)

    else:
        travelletterform = TravelletterForm(instance=travelletter)

    context = {
        "travelletterform": travelletterform,
        "travelletter": travelletter,
    }
    return render(request, "exchangepage/admindetail.html", context)


@permission_required("exchangepage.change_images")
def adminDetailImageViews(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    images = travelletter.images.all()

    if request.method == "POST":
        imageformset = ImageFormSet(
            files=request.FILES, data=request.POST, queryset=images
        )

        for form in imageformset:
            if form.is_valid():
                image = form.save(commit=False)
                image.travelletter = travelletter
                image.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            f"Bilder er oppdatert!",
            extra_tags="Suksess",
        )
        # Redirect to the desired page after successful editing
        return redirect("exchangepage:admindetailimage", pk=pk)

    else:
        imageformset = ImageFormSet(queryset=images)

    context = {"travelletter": travelletter, "imageformset": imageformset}
    return render(request, "exchangepage/admindetailimage.html", context)


@permission_required("exchangepage.change_experience")
def adminDetailExperienceViews(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    travelletter = experience.travelletter

    if request.method == "POST":
        experienceform = ExperienceForm(request.POST, instance=experience)

        if experienceform.is_valid():
            experience = experienceform.save(commit=False)
            experience.travelletter = travelletter
            experience.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Hele reisebrevet er oppdatert!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect(
                "exchangepage:createexperience", pk=travelletter.id
            )

    else:
        experienceform = ExperienceForm(instance=experience)

    context = {
        "experienceform": experienceform,
        "experience": experience,
        "travelletter": travelletter,
    }
    return render(request, "exchangepage/admindetailexperience.html", context)


@permission_required("exchangepage.change_travelletter")
def createQuestionViews(request):
    if request.method == "POST":
        questionform = QuestionsForm(request.POST)
        if questionform.is_valid():
            questionform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Nytt spørsmål opprettet!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect("exchangepage:adminquestion")

    else:
        questionform = QuestionsForm()

    context = {"questionform": questionform}
    return render(request, "exchangepage/createquestion.html", context)


@permission_required("exchangepage.change_travelletter")
def adminQuestionViews(request):
    questions = Questions.objects.all().order_by("id")
    context = {"questions": questions}
    return render(request, "exchangepage/adminquestion.html", context)


@permission_required("exchangepage.change_travelletter")
def adminQuestionDetailViews(request, pk):
    question = get_object_or_404(Questions, pk=pk)

    if request.method == "POST":
        questionform = QuestionsForm(request.POST, instance=question)
        if questionform.is_valid():
            questionform.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Spørsmålet er endret!",
                extra_tags="Suksess",
            )
            # Redirect to the desired page after successful editing
            return redirect("exchangepage:adminquestion")

    else:
        questionform = QuestionsForm(instance=question)
        print(questionform)

    context = {"questionform": questionform}
    return render(request, "exchangepage/adminquestiondetail.html", context)


@permission_required("exchangepage.delete_travelletter")
def deleteTravelletter(request, pk):
    query = Travelletter.objects.get(pk=pk)
    query.delete()

    messages.add_message(
        request,
        messages.WARNING,
        f"Reisebrev slettet!",
        extra_tags="Slettet",
    )
    return redirect("exchangepage:admin")


@permission_required("exchangepage.delete_experience")
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
    return redirect("exchangepage:createexperience", pk=travelletter.id)


@permission_required("exchangepage.delete_images")
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
    return redirect("exchangepage:admindetailimage", travelletter.id)


@login_required()
def displayIndividualLetter(request, pk):
    travelletter = get_object_or_404(Travelletter, pk=pk)
    experiences = Experience.objects.filter(travelletter=travelletter)
    questions = [experience.question for experience in experiences]
    images = Images.objects.filter(travelletter=travelletter)
    context = {}

    print(images)
    if images.exists():
        context["images"] = images

    specialization_id = travelletter.user.specialization - 1

    context["travelletter"] = travelletter
    context["experiences"] = experiences
    context["questions"] = questions
    context["images"] = images
    context["specialization_id"] = specialization_id
    context["specialization"] = SPECIALIZATION[specialization_id][1]

    return render(request, "exchangepage/detail.html", context)
