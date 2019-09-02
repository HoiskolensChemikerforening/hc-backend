from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from dal import autocomplete
from django.shortcuts import redirect, get_object_or_404
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import Pictureform, PictureTagForm
from .models import Contribution, PictureTag


@login_required
def submit_picture(request):
    form = Pictureform(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        form.save_m2m()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Bildet har blitt sendt inn!",
            extra_tags="Bildet ble sendt",
        )
        return redirect(reverse("carousel:submit"))
    context = {"form": form}

    return render(request, "picturecarousel/submit_picture.html", context)


def view_carousel(request):
    pictures = Contribution.objects.get_all_shuffled()
    context = {"pictures": pictures}
    return render(request, "picturecarousel/carousel.html", context)


@permission_required("picturecarousel.change_contribution")
def active_list(request, page=1):
    approved = Contribution.objects.filter(approved=True).prefetch_related(
        "author"
    ).order_by('-date')
    paginator = Paginator(approved, 10)

    try:
        picture_page = paginator.page(page)
    except PageNotAnInteger:
        picture_page = paginator.page(1)
        page = 1
    except EmptyPage:
        picture_page = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    MemberFormSet = modelformset_factory(
        Contribution, form=PictureTagForm, extra=0
    )
    approved_formset = MemberFormSet(
        request.POST or None, request.FILES or None, queryset=picture_page.object_list
    )

    if request.method == "POST":
        if approved_formset.is_valid():
            approved_formset.save()
        return redirect("carousel:active_detail", page)

    context = {"approved_formset": approved_formset,
               "picture_page": picture_page,
               "page": page
               }

    return render(request, "picturecarousel/tag_active.html", context)


@permission_required("picturecarousel.change_contribution")
def approve_pictures(request, page=1):
    awaiting_approval = Contribution.objects.filter(
        approved=False
    ).prefetch_related("author").order_by('-date')
    paginator = Paginator(awaiting_approval, 10)

    try:
        picture_page = paginator.page(page)
    except PageNotAnInteger:
        picture_page = paginator.page(1)
        page = 1
    except EmptyPage:
        picture_page = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    MemberFormSet = modelformset_factory(
        Contribution, form=PictureTagForm, extra=0
    )

    awaiting_formset = MemberFormSet(
        request.POST or None, request.FILES or None, queryset=picture_page.object_list
    )

    if request.method == "POST":
        if awaiting_formset.is_valid():
            awaiting_formset.save()
        return redirect("carousel:detail", page)

    context = {"awaiting_formset": awaiting_formset,
               "picture_page": picture_page,
               "page": page
               }

    return render(request, "picturecarousel/approve.html", context)


@permission_required("picturecarousel.change_contribution")
def approve_deny(request, picture_id, deny=False):
    picture = get_object_or_404(Contribution, id=picture_id)
    pictures_per_page = 10
    if not deny:
        awaiting_approval = Contribution.objects.filter(
            approved=False
        ).prefetch_related("author").order_by('-date')
        picture_index = list(awaiting_approval).index(picture)
        page = int(picture_index / pictures_per_page) + 1
        picture.approve()
        picture.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Bildet er godkjent",
            extra_tags="Yay!",
        )
        return redirect("carousel:detail", page)
    else:
        messages.add_message(
            request,
            messages.SUCCESS,
            "Bildet ble slettet",
            extra_tags="Slettet!",
        )
        if picture.approved:
            approved = Contribution.objects.filter(
                approved=True
            ).prefetch_related("author").order_by('-date')
            picture_index = list(approved).index(picture)
            page = int(picture_index / pictures_per_page) + 1
            picture.delete()
            return redirect("carousel:active_detail", page)
        else:
            awaiting_approval = Contribution.objects.filter(
                approved=False
            ).prefetch_related("author").order_by('-date')
            picture_index = list(awaiting_approval).index(picture)
            page = int(picture_index / pictures_per_page) + 1
            picture.delete()
            return redirect("carousel:detail", page)


class PictureTagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PictureTag.objects.none()

        qs = PictureTag.objects.all()

        if self.q:
            qs = qs.filter(tag__startswith=self.q) | qs.filter(tag__icontains=self.q)

        return qs.order_by('tag')

    def post(self, request):
        if request.user.has_perm("picturecarousel.add_picturetag"):
            return super(PictureTagAutocomplete, self).post(request)


@login_required
def view_pictures(request, page=1):
    if request.method == "POST":
        filter_form = PictureTagForm(request.POST)
        tags_ids = filter_form["tags"].value()
        tags = PictureTag.objects.filter(id__in=tags_ids).order_by('id')

        if tags:
            # Queryset for Contribution objects which contain ALL tags from POST request
            pictures = Contribution.objects.filter(
                approved=True,
                tags__in=tags
            ).annotate(num_tags=Count("tags")
                       ).filter(num_tags=tags.count()
                                ).prefetch_related("author").order_by('-date')

        else:
            pictures = Contribution.objects.filter(
                approved=True,
            ).prefetch_related("author").order_by('-date')

    else:
        if request.GET.get("tags"):
            tags_ids = request.GET.get("tags").split(",")
            tags = PictureTag.objects.filter(id__in=tags_ids).order_by('id')
            filter_form = PictureTagForm()
            filter_form.fields["tags"].queryset = tags
            pictures = Contribution.objects.filter(
                approved=True,
                tags__in=tags
            ).annotate(num_tags=Count("tags")
                       ).filter(num_tags=tags.count()
                                ).prefetch_related("author").order_by('-date')

        else:
            filter_form = PictureTagForm()
            pictures = Contribution.objects.filter(
                approved=True,
            ).prefetch_related("author").order_by('-date')

            tags_ids = []

    paginator = Paginator(pictures, 10)

    try:
        picture_page = paginator.page(page)
    except PageNotAnInteger:
        picture_page = paginator.page(1)
    except EmptyPage:
        picture_page = paginator.page(paginator.num_pages)

    context = {
        'filter_form': filter_form,
        'picture_page': picture_page,
        'tags': ",".join(tags_ids)
    }
    return render(request, 'picturecarousel/view_active.html', context)
