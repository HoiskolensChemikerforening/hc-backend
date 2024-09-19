from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import CGP, Group, Country
from .forms import GroupForm, CountryForm
from django.views import View
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.urls import reverse


@permission_required("cgp.add_cgp")
@login_required
def cgp_admin(request):
    """
    Renders the CGP main admin page.
    Args:
        request: HttpRequest
    Context:
        cgps: Queryset (All CGP objects orders by year in descending order)
        countries: (All Country objects)
    """
    cgps = CGP.objects.order_by("-year")
    countries = Country.objects.all()
    if request.method == "POST":  # brukeren trykker på knappen
        if not CGP.create_new_cgp():
            messages.add_message(
                request,
                messages.ERROR,
                f"Årets CGP finnes allerede!",
                extra_tags="Error",
            )
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Årets CGP har blitt opprettet!",
                extra_tags="Opprettet",
            )

    context = {"cgps": cgps, "countries": countries}
    return render(request, "cgp/admin/admin.html", context)


@permission_required("cgp.change_cgp")
@login_required
def cgp_edit(request, cgp_id):
    """
    Renders the page used to edit CGP objects.
    Args:
        request: HttpRequest
        cgp_id: int (id of the CGP object)
    Context:
        cgp: CGP object (CGP object with id cgp_id)
        groups: Queryset (all Group objects related to cgp)
    """
    cgp = get_object_or_404(CGP, id=cgp_id)
    groups = cgp.group_set.all()
    if request.method == "POST":
        cgp.toggle(request.user)
        return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))
    context = {"cgp": cgp, "groups": groups}
    return render(request, "cgp/admin/edit.html", context)


@permission_required("cgp.change_group")
@login_required
def group_edit(request, cgp_id, group_id):
    """
    Renders the forms page for the Group object and populates it with data from a group.
    Args:
        request: HttpRequest
        cgp_id: int (id of the CGP object)
        group_id: int (id of the Group object)
    Context:
        cgp: CGP object (CGP object with id cgp_id)
        object: Group object (Group object with id group_id)
        form: GroupForm (GroupForm object populated with group data)
        type: str (Gruppe)
    """
    cgp = get_object_or_404(CGP, id=cgp_id)
    group = get_object_or_404(Group, id=group_id)
    form = GroupForm(
        cgp, group, instance=group
    )  # , initial={"country": group.country})

    if request.method == "POST":
        form = GroupForm(
            cgp, group, request.POST, instance=group
        )  # , initial={"country": group.country})
        if form.is_valid():
            group = form.save(commit=False)
            group.cgp = cgp
            group.has_voted = False
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{str(group)} har blitt endret",
                extra_tags="Endret",
            )
            return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))
    context = {"object": group, "form": form, "type": "Gruppe", "cgp": cgp}
    return render(request, "cgp/admin/forms.html", context)


@permission_required("cgp.add_group")
@login_required
def group_add(request, cgp_id):
    """
    Renders the forms page for the Group object empty.
    Args:
        request: HttpRequest
        cgp_id: int (id of the CGP object)
    Context:
        cgp: CGP object (CGP object with id cgp_id)
        form: GroupForm (GroupForm object populated with group data)
        type: str (Gruppe)
    """
    cgp = get_object_or_404(CGP, id=cgp_id)
    form = GroupForm(cgp, None, request.POST or None)
    if form.is_valid():
        group = form.save(commit=False)
        group.cgp = cgp
        group.has_voted = False
        form.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"{str(group)} har blitt opprettet",
            extra_tags="Opprettet",
        )
        return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))

    context = {"form": form, "type": "Gruppe", "cgp": cgp}
    return render(request, "cgp/admin/forms.html", context)


@permission_required("cgp.change_country")
@login_required
def country_edit(request, country_id):
    """
    Renders the forms page for the Country object and populates it with data from a country.
    Args:
        request: HttpRequest
        country_id: int (id of the Country object)
    Context:
        object: Country object (Country object with id country_id)
        form: CountryForm (CountryForm object populated with country data)
        type: str (Land)
    """
    country = get_object_or_404(Country, id=country_id)
    form = CountryForm(instance=country)
    if request.method == "POST":
        form = CountryForm(
            request.POST or None, request.FILES or None, instance=country
        )
        if form.is_valid():
            country = form.save(commit=False)
            country.slug = slugify(country.country_name)
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{str(country)} har blitt endret",
                extra_tags="Endret",
            )
            return redirect(reverse("cgp:cgp_admin"))
    context = {"object": country, "form": form, "type": "Land"}
    return render(request, "cgp/admin/forms.html", context)


@permission_required("cgp.add_country")
@login_required
def country_add(request):
    """
    Renders the forms page for the Country object empty. And generates the slug attribute.
    Args:
        request: HttpRequest
    Context:
        form: CountryForm (CountryForm object populated with country data)
        type: str (Land)
    """
    form = CountryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        country = form.save(commit=False)
        country.slug = slugify(country.country_name)
        if not country.slug in Country.objects.values_list("slug", flat=True):
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{str(country)} har blitt opprettet",
                extra_tags="Opprettet",
            )
            return redirect(reverse("cgp:cgp_admin"))
        messages.add_message(
            request,
            messages.ERROR,
            f"{str(country)} likner for mye på {Country.objects.get(slug=country.slug)}",
            extra_tags="Error",
        )
    context = {"form": form, "type": "Land"}
    return render(request, "cgp/admin/forms.html", context)


class DeleteView(PermissionRequiredMixin, View):
    """
    Class based view to delete an object.
    Args:
        key: str (id of the object to be deleted (from link)
        objecttype: class (class of the object to be deleted)
        redirect_url: str (url name of the redirecting page)
    """

    key = None
    objecttype = None
    redirect_url = ""
    permission_required = ("cgp.delete_country", "cgp.delete_group")

    def get(self, request, *args, **kwargs):
        """
        Deletes an object and redirect to page.
        Args:
            self: DeleteView
            request: HttpRequest
            args: list (additional arguments as list)
            kwargs: dict (additional arguments from url as dict)
        Returns:
            redirects or redirect url
        """
        object = get_object_or_404(self.objecttype, id=kwargs.get(self.key))
        object_name = str(object)
        object.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"{object_name} ble slettet",
            extra_tags="Slettet",
        )
        kwargs.pop(self.key)
        return redirect(reverse(f"cgp:{self.redirect_url}", kwargs=kwargs))
