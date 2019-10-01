from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from django.utils import timezone

from rest_framework.permissions import AllowAny
from rest_framework import generics

from .models import Company, Interview
from .seralizers import CompanySerializer, InterviewSerializer

from chemie.committees.models import Committee
from chemie.events.models import Bedpres
from .forms import CreateCompanyForm, CreateInterviewForm


class ListCompany(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DetailCompany(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


"""
def index(request):
    indkom = Committee.objects.get(title="Industrikomiteen")
    bedpres = Bedpres.objects.filter(date__gte=timezone.now())
    context = {
        "indkom": indkom,
        "bedpres": bedpres,
    }
    return render(request, "corporate/index.html", context)


def company_list(request):
    companies = Company.objects.order_by("id")
    context = {"companies": companies}

    return render(request, "corporate/company_list.html", context)


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {"company": company}
    return render(request, "corporate/company_detail.html", context)


def company_create(request):
    form = CreateCompanyForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:company_list"))

    context = {"form": form}
    return render(request, "corporate/company_create.html", context)


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
"""