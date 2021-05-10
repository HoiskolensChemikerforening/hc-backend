from django.shortcuts import render
from .forms import MerchForm
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Merch
from django.contrib import messages


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


@login_required
def detail(request, pk):
    merch_object = get_object_or_404(Merch, id=pk)

    context = {"merch": merch_object}
    return render(request, "merch/detail.html", context)

@permission_required("merch.delete_merch")
def delete(request, pk):
    merch_object = get_object_or_404(Merch, id=pk)

    merch_object.delete()
    messages.add_message(
        request, messages.SUCCESS, "Merchen ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("merch:index"))