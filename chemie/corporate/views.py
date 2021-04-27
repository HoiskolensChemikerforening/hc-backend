from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Interview,
    JobAdvertisement,
    Specialization,
    Survey,
    AnswerKeyValuePair,
    SurveyQuestion,
)
from .forms import CreateQuestionForm

from chemie.committees.models import Committee
from chemie.events.models import Bedpres, Social

from .forms import (
    InterviewForm,
    CreateJobForm,
    CreateSurveyForm,
    CreateAnswerForm,
)


def index(request):
    indkom = Committee.objects.get(title="Industrikomiteen")

    bedpres = Bedpres.objects.filter(date__gte=timezone.now()).order_by("date")
    events = Social.objects.filter(
        date__gte=timezone.now(), committee=indkom
    ).order_by("date")

    no_events = (not bedpres.exists()) and (not events.exists())

    context = {
        "indkom": indkom,
        "bedpres": bedpres,
        "events": events,
        "no_events": no_events,
    }

    return render(request, "corporate/index.html", context)


def job_advertisement(request):
    job_advertisements = JobAdvertisement.objects.filter(
        is_published=True
    ).order_by("published_date")

    context = {"job_advertisements": job_advertisements}
    return render(request, "corporate/job_advertisement.html", context)


def interview(request):
    interviews = Interview.objects.all().order_by("-id")
    min_year = interviews.order_by("graduation_year").first().graduation_year
    max_year = interviews.order_by("graduation_year").last().graduation_year

    if request.method == "GET":
        if request.GET.get("minyear"):
            try:
                min_filter_year = int(request.GET.get("minyear"))
                interviews = interviews.filter(
                    graduation_year__gte=min_filter_year
                )
            except ValueError:
                min_filter_year = min_year
        else:
            min_filter_year = min_year

        if request.GET.get("maxyear"):
            try:
                max_filter_year = int(request.GET.get("maxyear"))
                interviews = interviews.filter(
                    graduation_year__lte=max_filter_year
                )
            except ValueError:
                max_filter_year = max_year
        else:
            max_filter_year = max_year

        if request.GET.getlist("specialization"):
            try:
                specializations = [
                    int(x) for x in request.GET.getlist("specialization")
                ]
                interviews = interviews.filter(
                    specializations__name__in=specializations
                ).distinct()
            except ValueError:
                pass
    else:
        min_filter_year = min_year
        max_filter_year = max_year

    specializations = Specialization.objects.all().order_by("id")

    context = {
        "interviews": interviews,
        "min_year": min_year,
        "max_year": max_year,
        "min_filter_year": min_filter_year,
        "max_filter_year": max_filter_year,
        "specializations": specializations,
    }
    return render(request, "corporate/interview.html", context)


def interview_detail(request, id):
    interview = get_object_or_404(Interview, pk=id)

    context = {"interview": interview}
    return render(request, "corporate/interview_detail.html", context)


def survey(request, year=None):
    if year is None:
        try:
            year = Survey.objects.latest("year").year
            survey = Survey.objects.get(year=year)
            q_a_dict = survey.get_q_a_dict()
        except:
            survey = None
            q_a_dict = None
    else:
        survey = get_object_or_404(Survey, year=year)
        q_a_dict = survey.get_q_a_dict()

    all_surveys = Survey.objects.all()

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
    form = InterviewForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:interview"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)


@permission_required("corporate.delete_interview")
def interview_delete(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.delete()
    return redirect("corporate:interview")


@permission_required("corporate.edit_article")
def interview_edit(request, id):
    interview = get_object_or_404(Interview, id=id)
    form = InterviewForm(
        request.POST or None, request.FILES or None, instance=interview
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("corporate:interview"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)


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
    surveys = Survey.objects.all().order_by("-year")

    form = CreateSurveyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:statistics_admin"))

    context = {"surveys": surveys, "form": form}

    return render(request, "corporate/statistics_admin.html", context)


@permission_required("corporate.add_survey")
def survey_edit(request, year):
    survey = get_object_or_404(Survey, year=year)
    q_a_dict = survey.get_q_a_dict()

    # Display dict = {question: zip(choices, values, ids)}
    display_dict = {}
    for q in q_a_dict.keys():
        display_dict[q] = zip(
            q_a_dict[q]["choices"], q_a_dict[q]["values"], q_a_dict[q]["ids"]
        )

    context = {"survey": survey, "q_a_dict": display_dict}
    return render(request, "corporate/survey_edit.html", context)


@permission_required("corporate.change_survey")
def survey_remove_question(request):
    if request.method == "POST":
        survey_id = request.POST["id"]
        question = request.POST["question"]
        survey = get_object_or_404(Survey, id=survey_id)
        survey_question = get_object_or_404(SurveyQuestion, question=question)

        # Remove all AnswerKeyValuePairs linked to this survey and this question
        AnswerKeyValuePair.objects.filter(survey=survey).filter(
            question=survey_question
        ).delete()

        return JsonResponse({"success": True})

    else:
        return redirect("corporate:statistics_admin")


@permission_required("corporate:delete_survey")
def survey_delete(request, year):
    if request.method == "POST":
        survey = get_object_or_404(Survey, year=year)
        survey.delete()

    return redirect("corporate:statistics_admin")


@permission_required("corporate:add_surveyquestion")
def question_create(request):
    form = CreateQuestionForm(request.POST or None)
    questions = SurveyQuestion.objects.all().order_by("question")
    if request.method == "POST":
        if form.is_valid():
            form.save()

            if request.POST["next"]:
                next = request.POST["next"]
                return redirect(next)

    context = {"questions": questions, "form": form}

    return render(
        request, "corporate/statistics_question_create.html", context
    )


@permission_required("corporate:change_surveyquestion")
def question_edit(request):
    if request.method == "POST":
        id = request.POST["id"]
        edited_question = request.POST["question"]
        question = get_object_or_404(SurveyQuestion, id=id)
        question.question = edited_question
        question.save()
        return JsonResponse({"success": True})

    else:
        return redirect("corporate:statistics")


@permission_required("corporate:delete_surveyquestion")
def question_delete(request, id):
    if request.method == "POST":
        question = get_object_or_404(SurveyQuestion, id=id)
        question.delete()
        return redirect("corporate:question_create")

    else:
        return redirect("corporate:statistics")


@permission_required("corporate:add_surveyquestion")
def add_question_to_survey(request, year):
    survey = get_object_or_404(Survey, year=year)

    if request.method == "POST":
        for key, value in request.POST.items():
            if "checkbox" in key:
                question = get_object_or_404(
                    SurveyQuestion, question=request.POST[key]
                )
                # The way the database is organized now, a survey can't be
                # linked to a surveyquestion without there being any
                # answers. This creates a placeholder answer so it
                # shows up on the survey admin page
                default_answer = AnswerKeyValuePair.objects.create(
                    key="Placeholder for svaralternativ",
                    value=0,
                    question=question,
                    survey=survey,
                )
                default_answer.save()
        return redirect("corporate:survey_edit", year)

    survey_questions = survey.get_q_a_dict().keys()
    all_questions = SurveyQuestion.objects.values_list("question", flat=True)

    questions = []
    for question in all_questions:
        if question not in survey_questions:
            questions.append(question)

    context = {"survey": survey, "questions": questions}

    return render(request, "corporate/statistics_add_question.html", context)


@permission_required("corporate:add_answerkeyvaluepair")
def answer_create(request, year, question):
    survey = get_object_or_404(Survey, year=year)
    question = get_object_or_404(SurveyQuestion, question=question)
    form = CreateAnswerForm(request.POST or None)

    # Survey and question fields are already determined and can't be changed
    form.fields.pop("survey")
    form.fields.pop("question")

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            new_answer = AnswerKeyValuePair(
                key=data["key"],
                value=data["value"],
                question=question,
                survey=survey,
            )
            new_answer.save()
            return redirect("corporate:survey_edit", year=survey.year)

    context = {"survey": survey, "question": question, "form": form}
    return render(request, "corporate/statistics_answer_create.html", context)


@permission_required("corporate:change_answerkeyvaluepair")
def answer_edit(request):
    if request.method == "POST":
        id = request.POST["id"]
        value = request.POST["value"]
        answer = request.POST["answer"]

        answer_value_pair = get_object_or_404(AnswerKeyValuePair, id=id)
        answer_value_pair.value = value
        answer_value_pair.key = answer

        answer_value_pair.save()

        return JsonResponse({"success": True})
    else:
        return redirect("corporate:statistics")


@permission_required("corporate.delete_answerkeyvaluepair")
def answer_delete(request, id):
    if request.method == "POST":
        answer = get_object_or_404(AnswerKeyValuePair, id=id)
        survey = answer.survey
        answer.delete()

        return redirect("corporate:survey_edit", year=survey.year)

    return redirect("corporate:index")
