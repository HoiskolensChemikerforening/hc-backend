from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect, reverse
from .models import Company, Interview
from .forms import CreateCompanyForm

# Create your views here.


def index(request):
    return HttpResponse("Du er sykt heft10")


def interview(request):
    interviews = Interview.objects.order_by("id")
    context = {"interviews": interviews}

    return render(request, "corporate/interview.html", context)


def create_company(request):
    form = CreateCompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("corporate:temp_company_list"))

    context = {"form": form}
    return render(request, "corporate/company_create.html", context)
