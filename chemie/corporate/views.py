from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect

from .models import Interview, Job, Specialization

from chemie.committees.models import Committee
from chemie.events.models import Bedpres, Social
from .forms import InterviewForm, JobForm


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


def job(request):
    jobs = Job.objects.all().order_by("-id")

    if request.method == "GET":
        if request.GET.getlist("specialization"):
            try:
                specializations = [
                    int(x) for x in request.GET.getlist("specialization")
                ]
                jobs = jobs.filter(
                    specializations__name__in=specializations
                ).distinct()
            except ValueError:
                pass

    specializations = Specialization.objects.all().order_by("id")

    context = {
        "jobs": jobs,
        "specializations": specializations,
    }
    return render(request, "corporate/job.html", context)


def job_detail(request, id):
    job = get_object_or_404(Job, pk=id)

    context = {"job": job}
    return render(request, "corporate/job_detail.html", context)


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


def statistics(request):
    context = {}
    return render(request, "corporate/statistics.html", context)


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


@permission_required("corporate.add_job")
def job_create(request):
    form = JobForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:job"))

    context = {"form": form}
    return render(request, "corporate/job_create.html", context)


@permission_required("corporate.delete_job")
def job_delete(request, id):
    job = get_object_or_404(Job, id=id)
    job.delete()

    return redirect("corporate:job")


@permission_required("corporate.edit_article")
def job_edit(request, id):
    job = get_object_or_404(Job, id=id)
    form = JobForm(
        request.POST or None, request.FILES or None, instance=job
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("corporate:job"))

    context = {"form": form}
    return render(request, "corporate/job_edit.html", context)
