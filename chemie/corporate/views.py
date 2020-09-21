from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from django.utils import timezone

from .models import Interview, JobAdvertisement

from chemie.committees.models import Committee
from chemie.events.models import Bedpres
from .forms import CreateInterviewForm


def index(request):
    indkom = Committee.objects.get(title="Industrikomiteen")
    bedpres = Bedpres.objects.filter(date__gte=timezone.now()).order_by("date")
    job_advertisements = JobAdvertisement.objects.filter(is_current=True).order_by(
        "published_date"
    )
    interviews = Interview.objects.all().order_by("id")
    context = {
        "indkom": indkom,
        "bedpres": bedpres,
        "job_advertisements": job_advertisements,
        "interviews": interviews
    }
    return render(request, "corporate/index.html", context)


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


def interview_create(request):
    form = CreateInterviewForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:interview_list"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)
