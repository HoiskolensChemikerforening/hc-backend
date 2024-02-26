from django.shortcuts import render
from .forms import MerchForm, MerchCategoryForm, SortingForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Merch, MerchCategory
from django.contrib import messages
from dal import autocomplete
from django.utils.html import format_html


@permission_required("merch.add_merch")
def create_merch(request):
    form = MerchForm(request.POST or None, request.FILES or None)

    if request.POST:
        if "another" in request.POST and form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Merchen ble opprettet",
                extra_tags="Opprettet",
            )
            return HttpResponseRedirect(reverse("merch:create"))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Merchen ble opprettet",
                extra_tags="Opprettet",
            )
            return HttpResponseRedirect(reverse("merch:index"))

    context = {"form": form}

    return render(request, "merch/create_merch.html", context)


@permission_required("merch.add_merch")
def create_category(request):
    form = MerchCategoryForm(request.POST or None, request.FILES or None)

    if request.POST:
        if "another" in request.POST and form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Kategorien ble opprettet",
                extra_tags="Opprettet",
            )
            return HttpResponseRedirect(reverse("merch:create_category"))

        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Kategorien ble opprettet",
                extra_tags="Opprettet",
            )
            return HttpResponseRedirect(reverse("merch:index"))

    context = {"form": form}

    return render(request, "merch/create_category.html", context)


@login_required
def all_merch(request):
    merch_objects = Merch.objects.all().order_by("name")
    form = SortingForm()

    if not merch_objects.exists():
        return render(request, "merch/empty.html")
    else:

        if request.method == "POST":
            form = SortingForm(request.POST)
            if form.is_valid():
                if request.POST["submit"] != "Nullstill":
                    merch_objects = Merch.objects.filter(
                        category=form.cleaned_data["category"]
                    )
    obj_per_page = 25  # Show 25 contacts per page.
    if len(merch_objects) < obj_per_page:
        context = {"merchs": merch_objects, "form": form}
    else:
        paginator = Paginator(merch_objects, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"merchs": page_obj, "form": form}

    return render(request, "merch/list_all.html", context)


@login_required
def detail(request, pk):
    merch_object = get_object_or_404(Merch, id=pk)
    context = {"merch": merch_object}
    return render(request, "merch/detail.html", context)


@login_required
def detail_category(request):
    categories = MerchCategory.objects.all()
    context = {"categories": categories}
    return render(request, "merch/list_all_categories.html", context)


@permission_required("merch.delete_merch")
def delete(request, pk):
    merch_object = get_object_or_404(Merch, id=pk)

    merch_object.delete()
    messages.add_message(
        request, messages.SUCCESS, "Merchen ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("merch:index"))


@permission_required("merch.delete_merchcategories")
def delete_categories(request, merchcategory_id):
    category_object = get_object_or_404(MerchCategory, id=merchcategory_id)

    category_object.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        "Kategorien ble slettet",
        extra_tags="Slettet",
    )
    return HttpResponseRedirect(reverse("merch:categories"))


@permission_required("merch.change_merchcategories")
def edit_category(request, merchcategory_id):
    category = get_object_or_404(MerchCategory, id=merchcategory_id)
    form = MerchCategoryForm(request.POST or None, instance=category)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Kategorien ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("merch:categories"))
    context = {"form": form}
    return render(request, "merch/create_category.html", context)


@permission_required("merch.change_merch")
def edit_merch(request, pk):
    merch_object = get_object_or_404(Merch, id=pk)
    form = MerchForm(
        request.POST or None, request.FILES or None, instance=merch_object
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Merchen ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("merch:index"))
    context = {"form": form}
    return render(request, "merch/create_merch.html", context)


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return MerchCategory.objects.none()

        qs = MerchCategory.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

    def get_result_label(self, category):
        return format_html("{}", category.name)
