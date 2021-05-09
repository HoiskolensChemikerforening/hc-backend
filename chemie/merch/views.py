from django.shortcuts import render
from .forms import MerchForm
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Merch

# Create your views here.
@permission_required("merch.add_merch")
def create_merch(request):
    form = MerchForm(request.POST or None, request.FILES or None)

    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse("merch:index"))

    context = {"form": form}

    return render(request, "merch/create_merch.html", context)


@login_required
def all_merch(request):
    merch_objects = Merch.objects.all()

    context = {"merchs": merch_objects}
    return (render(request, "merch/list_all.html", context))