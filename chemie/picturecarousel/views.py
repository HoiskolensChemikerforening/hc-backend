from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from dal import autocomplete
from django.shortcuts import redirect, get_object_or_404
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from .forms import Pictureform, PictureTagForm
from .models import Contribution, PictureTag
from django.utils.html import format_html
from django.forms import modelformset_factory


# TODO: Fikse submit picture form, save tags before godkjenn? Mulig å submitte begge?
#  JA, for burde ha mulighet itl å legge til tags etter submitted
#

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
def approve_pictures(request):
    awaiting_approval = Contribution.objects.filter(
        approved=False
    ).prefetch_related("author")
    approved = Contribution.objects.filter(approved=True).prefetch_related(
        "author"
    )
    context = {"awaiting_approval": awaiting_approval, "approved": approved}
    return render(request, "picturecarousel/approve.html", context)


@permission_required("picturecarousel.change_contribution")
def approve_deny(request, picture_id, deny=False):
    if request.method == "POST":
        picture = get_object_or_404(Contribution, id=picture_id)
        if not deny:
            picture.approve()
            picture.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Bildet er godkjent",
                extra_tags="Yay!",
            )
        else:
            picture.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Bildet ble slettet",
                extra_tags="Slettet!",
            )
        return HttpResponseRedirect(reverse("carousel:overview"))
    return HttpResponseRedirect(reverse("carousel:overview"))


class PictureTagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PictureTag.objects.none()

        qs = PictureTag.objects.all()

        if self.q:
            qs = qs.filter(tag__startswith=self.q) | qs.filter(tag__icontains=self.q)

        return qs
