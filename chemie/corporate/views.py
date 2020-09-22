from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required

from .models import Interview, JobAdvertisement

from chemie.committees.models import Committee
from chemie.events.models import Bedpres
from .forms import CreateInterviewForm, CreateJobForm


def index(request):
    indkom = Committee.objects.get(title="Industrikomiteen")
    bedpres = Bedpres.objects.filter(date__gte=timezone.now()).order_by("date")
    job_advertisements = JobAdvertisement.objects.filter(
        is_current=True
    ).order_by("published_date")
    interviews = Interview.objects.all().order_by("id")
    context = {
        "indkom": indkom,
        "bedpres": bedpres,
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
def interview_delete(request, id):
    interview = get_object_or_404(Interview, id=id)
    interview.delete()
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
def job_delete(request, id):
    job = get_object_or_404(JobAdvertisement, id=id)
    job.delete()
    return redirect("corporate:index")


"""
def interview_list(request):
    interviews = Interview.objects.order_by("id")
    context = {
        "interviews": interviews
    }
    return render(request, "corporate/interview_list.html", context)


def interview_detail(request, interview_id):
    this_interview = get_object_or_404(Interview, id=interview_id)
    context = {"interview": this_interview}
    return render(request, "corporate/interview_detail.html", context)
"""
