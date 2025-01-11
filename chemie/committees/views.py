from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from django.db.models import Q

from .forms import EditDescription, EditPositionForm
from .models import Committee, Position

from .serializers import CommitteeSerializer, PositionSerializer
from rest_framework import generics


def index(request):
    # Fetch all members, who belong to a committee (Member -> Committee)
    # Group all these members by the committee type
    committees = Committee.objects.order_by("title")
    context = {"committees": committees}

    return render(request, "committees/list_committees.html", context)


def view_committee(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    positions = Position.objects.filter(committee=committee).prefetch_related(
        "users"
    )
    context = {"committee": committee, "positions": positions}
    return render(request, "committees/view_committee.html", context)


@permission_required("committees.change_committee")
def email_download_view(request, slug):
    template_name = "committees/email_download.html"
    committee = get_object_or_404(Committee, slug=slug)

    # check permissions
    no_permissions, redirect_target = check_if_admin_of_group(
        request, committee, slug
    )
    if no_permissions:
        return redirect_target

    positions = Position.objects.filter(committee=committee).prefetch_related(
        "users"
    )
    members = []
    for position in positions:
        members.extend(position.users.all())

    members = list(set(members))
    context = {"members": members, "committee": committee}

    return render(request, template_name, context)


def check_if_admin_of_group(request, committee, slug):
    """
    Checks if the current user is has permissions to edit the current committee.
    Redirects the user if not.
    """
    managers = Position.objects.filter(
        can_manage_committee=True, committee=committee
    )
    admin_of_this_group = any(
        [request.user in p.users.all() for p in managers]
    )
    enough_perms = admin_of_this_group or request.user.has_perm(
        "committees.add_committee"
    )
    if not enough_perms:
        messages.add_message(
            request,
            messages.ERROR,
            "Du har bare lov å endre egne undergrupper.",
            extra_tags="Manglende rettigheter!",
        )
        return True, redirect(
            reverse("verv:committee_detail", kwargs={"slug": slug})
        )
    return False, None


@permission_required("committees.change_committee")
def edit_description(request, slug):
    committee = get_object_or_404(Committee, slug=slug)

    # check permissions
    no_permissions, redirect_target = check_if_admin_of_group(
        request, committee, slug
    )
    if no_permissions:
        return redirect_target

    form = EditDescription(
        request.POST or None, request.FILES or None, instance=committee
    )
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "{} har blitt endret!".format(committee.title),
                extra_tags="Supert",
            )
            return HttpResponseRedirect(committee.get_absolute_url())
    context = {"committee": committee, "form": form}
    return render(request, "committees/edit_description.html", context)


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        for term in self.q.split():
            qs = qs.filter(
                Q(first_name__icontains=term) | Q(last_name__icontains=term)
            ) | qs.filter(username__icontains=self.q)
        return qs

    def get_result_label(self, user):
        return format_html("{}", user.get_full_name())


@permission_required("committees.change_committee")
def edit_committee_memberships(request, slug):
    positions = Position.objects.filter(committee__slug=slug)
    managers = positions.filter(can_manage_committee=True)

    # A user may have change_committee permission,
    # but must have "add_position" to edit all committees or be
    # an administrator of the committee
    admin_of_this_group = any(
        [request.user in p.users.all() for p in managers]
    )
    enough_perms = admin_of_this_group or request.user.has_perm(
        "committees.add_position"
    )
    if not (enough_perms):
        messages.add_message(
            request,
            messages.ERROR,
            "Du har bare lov å endre egne undergrupper.",
            extra_tags="Manglende rettigheter!",
        )
        return redirect(
            reverse("verv:committee_detail", kwargs={"slug": slug})
        )

    MemberFormSet = modelformset_factory(
        Position, form=EditPositionForm, extra=0
    )

    formset = MemberFormSet(
        request.POST or None, request.FILES or None, queryset=positions
    )

    if request.method == "POST":
        if formset.is_valid():
            formset.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Endringene ble lagret.",
                extra_tags="Flott!",
            )
            committee = get_object_or_404(Committee, slug=slug)
            return HttpResponseRedirect(committee.get_absolute_url())
    else:
        for form in formset:
            # Dynamically change each max-selected-items
            # according to the positions' max_members
            form.fields.get("users").widget.attrs[
                "data-maximum-selection-length"
            ] = form.instance.max_members
    context = {"formset": formset, "committee": slug}
    return render(request, "committees/edit_committee_members.html", context)


class ListAllCommittees(generics.ListCreateAPIView):
    queryset = Committee.objects.all().order_by("title")
    serializer_class = CommitteeSerializer


class CommitteeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer


class ListAllPositions(generics.ListCreateAPIView):
    queryset = Position.objects.all().order_by("committee")
    serializer_class = PositionSerializer


class PositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all().order_by("committee")
    serializer_class = PositionSerializer
