from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.utils import timezone

from .models import Company, Interview
from chemie.committees.models import Committee
from chemie.events.models import Bedpres
from .forms import CreateCompanyForm, CreateInterviewForm

# Create your views here.


def index(request):
    indkom = Committee.objects.get(id=12)
    bedpres = Bedpres.objects.filter(date__gte=timezone.now())
    context = {
        "indkom": indkom,
        "bedpres": bedpres,
    }
    return render(request, "corporate/index.html", context)


def interview(request):
    interviews = Interview.objects.order_by("id")
    context = {"interviews": interviews}

    return render(request, "corporate/interview.html", context)


def list_companies(request):
    companies = Company.objects.order_by("id")
    context = {"companies": companies}

    return render(request, "corporate/list_companies.html", context)

def create_company(request):
    form = CreateCompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:temp_company_list"))

    context = {"form": form}
    return render(request, "corporate/company_create.html", context)


def create_interview(request):
    form = CreateInterviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("interview:temp_interview_list"))

    context = {"form": form}
    return render(request, "corporate/interview_create.html", context)
