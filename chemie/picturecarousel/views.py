from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from dal import autocomplete
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import Pictureform, PictureTagForm
from .models import Contribution, PictureTag
from django.forms import modelformset_factory


# TODO: Render tag field in submit PictureForm

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

    MemberFormSet = modelformset_factory(
        Contribution, form=PictureTagForm, extra=0
    )

    awaiting_formset = MemberFormSet(
        request.POST or None, request.FILES or None, queryset=awaiting_approval
    )
    approved_formset = MemberFormSet(
        request.POST or None, request.FILES or None, queryset=approved
    )

    if request.method == "POST":
        if 'save_tag' in request.POST:
            if awaiting_formset.is_valid():
                awaiting_formset.save()

            if approved_formset.is_valid():
                approved_formset.save()

            return redirect("carousel:overview")

        elif 'approve' in request.POST:
            picture_id = request.POST.get('form-0-id')
            return redirect("carousel:approve", picture_id)

        elif 'delete' in request.POST:
            picture_id = request.POST.get('form-0-id')
            return redirect("carousel:deny", picture_id)

        return redirect("carousel:overview")

    context = {"awaiting_approval": awaiting_approval,
               "approved": approved,
               "awaiting_formset": awaiting_formset,
               "approved_formset": approved_formset
               }

    return render(request, "picturecarousel/approve.html", context)


@permission_required("picturecarousel.change_contribution")
def approve_deny(request, picture_id, deny=False):
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


class PictureTagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PictureTag.objects.none()

        qs = PictureTag.objects.all()

        if self.q:
            qs = qs.filter(tag__startswith=self.q) | qs.filter(tag__icontains=self.q)

        return qs
