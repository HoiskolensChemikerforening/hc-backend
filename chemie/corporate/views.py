from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required

from .models import Interview, JobAdvertisement

from chemie.committees.models import Committee
from chemie.events.models import Bedpres, Social
from .forms import CreateInterviewForm, CreateJobForm


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

    context = {
        "job_advertisements": job_advertisements,
    }
    return render(request, "corporate/job_advertisement.html", context)


def interview(request):
    interviews = Interview.objects.filter(is_published=True).order_by("-id")

    context = {
        "interviews": interviews,
    }
    return render(request, "corporate/interview.html", context)


def interview_detail(request, id):
    interview = get_object_or_404(Interview, pk=id)

    context = {
        "interview": interview,
    }
    return render(request, "corporate/interview_detail.html", context)


def statistics(request):
    context = {}
    return render(request, "corporate/statistics.html", context)


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
