from django.shortcuts import render
from .forms import MerchForm, MerchCategoryForm
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Merch, MerchCategory
from django.contrib import messages
from dal import autocomplete
from django.utils.html import format_html

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

@permission_required("merch.add_merch")
def create_category(request):
    form = MerchCategoryForm(request.POST or None, request.FILES or None)

    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse("merch:index"))

    context = {"form": form}

    return render(request, "merch/create_category.html", context)


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


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return MerchCategory.objects.none()

        qs = MerchCategory.objects.all()

        """
        if self.q:
            qs = (
                qs.filter(username__icontains=self.q)
                | qs.filter(first_name__icontains=self.q)
                | qs.filter(last_name__icontains=self.q)
            )
        """

        return qs

    def get_result_label(self, category):
        return format_html("{}", category.name)
