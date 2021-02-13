from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Interview, JobAdvertisement, Survey

from chemie.committees.models import Committee
from chemie.events.models import Bedpres, Social
from .forms import (
    CreateInterviewForm,
    CreateJobForm,
    CreateSurveyForm,
    CreateQuestionForm,
    CreateAnswerForm,
)


def index(request):
    indkom = Committee.objects.get(title="Industrikomiteen")

    bedpres = Bedpres.objects.filter(date__gte=timezone.now()).order_by("date")
    events = Social.objects.filter(
        date__gte=timezone.now(), committee=indkom
    ).order_by("date")

    no_events = (not bedpres.exists()) and (not events.exists())

    job_advertisements = JobAdvertisement.objects.filter(
        is_published=True
    ).order_by("published_date")

    interviews = Interview.objects.filter(is_published=True).order_by("id")

    context = {
        "indkom": indkom,
        "bedpres": bedpres,
        "events": events,
        "no_events": no_events,
        "job_advertisements": job_advertisements,
        "interviews": interviews,
    }

    return render(request, "corporate/index.html", context)


def job_advertisement(request):
    job_advertisements = JobAdvertisement.objects.filter(
        is_published=True
    ).order_by("published_date")

    context = {"job_advertisements": job_advertisements}
    return render(request, "corporate/job_advertisement.html", context)


def interview(request):
    interviews = Interview.objects.filter(is_published=True).order_by("-id")

    context = {"interviews": interviews}
    return render(request, "corporate/interview.html", context)


def interview_detail(request, id):
    interview = get_object_or_404(Interview, pk=id)

    context = {"interview": interview}
    return render(request, "corporate/interview_detail.html", context)


def survey(request, year=None):
    if year is None:
        year = Survey.objects.latest("year").year

    all_surveys = Survey.objects.all()
    survey = Survey.objects.get(year=year)
    q_a_dict = survey.get_q_a_dict()

    context = {
        "all_surveys": all_surveys,
        "survey": survey,
        "q_a_dict": q_a_dict,
    }

    return render(request, "corporate/statistics.html", context)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        survey = get_object_or_404(Survey, id=id)
        data = survey.get_q_a_dict()
        return Response(data)


@permission_required("corporate.add_interview")
def interview_create(request):
    form = CreateInterviewForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:interview"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)


@permission_required("corporate.delete_interview")
def interview_remove(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.is_published = False
    interview.save()

    return redirect("corporate:interview")


@permission_required("corporate.add_jobadvertisement")
def job_create(request):
    form = CreateJobForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:job_advertisement"))

    context = {"form": form}
    return render(request, "corporate/job_create.html", context)


@permission_required("corporate.delete_jobadvertisement")
def job_remove(request, id):
    job = get_object_or_404(JobAdvertisement, id=id)
    job.is_published = False
    job.save()

    return redirect("corporate:job_advertisement")


@permission_required("corporate.add_survey")
def statistics_admin(request):
    return render(request, "corporate/statistics_admin.html")


@permission_required("corporate.add_survey")
def survey_edit(request):
    return render(request, "corporate/survey_edit.html")


@permission_required("corporate.add_survey")
def survey_create(request):
    return render(request, "corporate/survey_create.html")


# TODO: Sjekk at permission er riktig
@permission_required("corporate.add_surveyquestion")
def question_create(request):
    return render(request, "corporate/question_create.html")


# TODO: Sjekk at permission er riktig
@permission_required("corporate.add_answerkeyvaluepair")
def answer_create(request):
    return render(request, "corporate/answer_create.html")


# Template 1 = statistics_admin: "Diplomundersøkelsen > Admin" Admin page: Liste over alle surveys.
#       - Kan ta + for å lage ny survey (altså nytt år)
# Template 2 = survey_create.html: Lage ny survey
# Template 3 = survey_detail.html: "Diplomundersøkelsen > Admin > 20XX" Valgt survey: List alle spørsmål
#       - Velg å legge til nytt spørsmål til denne surveyen (selectmultiple)
#       - Velg å lage et nytt spørsmål
# Template 4 = question_create.html: "Diplomundersøkelsen > Admin > Nytt spørsmål" Lage nytt spørsmål
#       - Redirect til survey?
# Template 5 = answer_create.html: "Diplomundersøkelsen > Admin > År > Spørsmål
#       - Legge til nye svar på gitt spørsmål
