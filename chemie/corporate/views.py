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


@permission_required("corporate.add_interview")
def interview_create(request):
    form = CreateInterviewForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:index"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)


@permission_required("corporate.delete_interview")
def interview_remove(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.is_published = False
    interview.save()

    return redirect("corporate:index")


@permission_required("corporate.add_jobadvertisement")
def job_create(request):
    form = CreateJobForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:index"))

    context = {"form": form}
    return render(request, "corporate/job_create.html", context)


@permission_required("corporate.delete_jobadvertisement")
def job_remove(request, id):
    job = get_object_or_404(JobAdvertisement, id=id)
    job.is_published = False
    job.save()

    return redirect("corporate:index")