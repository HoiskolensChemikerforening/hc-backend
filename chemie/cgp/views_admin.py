from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import CGP,Group, Country
from .forms import CGPForm, GroupForm, CountryForm
from django.core.exceptions import ValidationError
from django.views import View
from django.template.defaultfilters import slugify
from django.contrib import messages

from django.urls import path, reverse
@permission_required("elections.add_election")
@login_required
def cgp_admin(request):
    cgps = CGP.objects.all()
    countries = Country.objects.all()
    if request.method == "POST":  # brukeren trykker på knappen
        CGP.create_new_cgp()


    context = {
        "cgps": cgps,
        "countries": countries
    }
    return render(request, "cgp/admin/admin.html", context)



@permission_required("elections.add_election")
@login_required
def cgp_edit(request, cgp_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    groups = cgp.group_set.all()
    countries = Country.objects.all()
    if request.method == "POST":
        cgp.toggle(request.user)
        return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))
    context = {
        "cgp": cgp,
        "groups": groups,
        "countries": countries
    }
    return render(request, "cgp/admin/edit.html", context)

def group_edit(request, cgp_id, group_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    group = get_object_or_404(Group, id=group_id)
    form = GroupForm(cgp, group, instance=group)#, initial={"country": group.country})

    if request.method == "POST":
        form = GroupForm(cgp, group, request.POST, instance=group)#, initial={"country": group.country})
        if form.is_valid():
            group = form.save(commit=False)
            group.cgp = cgp
            group.has_voted = False
            form.save()
            messages.add_message(
                request, messages.SUCCESS, f"{str(group)} har blitt endret", extra_tags="Endret"
            )
            return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))
    context = {
        "cgp": cgp,
        "group": group,
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

def group_add(request, cgp_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    form = GroupForm(cgp,None, request.POST or None)
    if form.is_valid():
        group = form.save(commit=False)
        group.cgp = cgp
        group.has_voted = False
        form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{str(group)} har blitt opprettet", extra_tags="Opprettet"
        )
        return redirect(reverse("cgp:cgp_edit", kwargs={"cgp_id": cgp_id}))


    context = {
        "cgp": cgp,
        "form": form,
    }
    return render(request, "cgp/admin/forms.html", context)

def country_edit(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    form = CountryForm(instance=country)
    if request.method == "POST":
        form = CountryForm(request.POST or None, request.FILES or None, instance=country)
        if form.is_valid():
            country = form.save(commit=False)
            country.slug = slugify(country.country_name)
            form.save()
            messages.add_message(
                request, messages.SUCCESS, f"{str(country)} har blitt endret", extra_tags="Endret"
            )
            return redirect(reverse("cgp:cgp_admin"))
    context = {
        "country": country,
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

def country_add(request):
    form = CountryForm(request.POST or None, request.FILES or None)
    #field = form.fields["slug"]
    #field. = slugify(country.country_name)
    #field.widget = field.hidden_widget()
    if form.is_valid():
        country = form.save(commit=False)
        country.slug = slugify(country.country_name)
        #print(form.is_valid())
        #if len(Country.objects.filter(slug=country.slug))> 0:
         #   raise ValidationError("Ugyldig navn")
        form.save()
        messages.add_message(
            request, messages.SUCCESS, f"{str(country)} har blitt opprettet", extra_tags="Opprettet"
        )
        return redirect(reverse("cgp:cgp_admin"))
    context = {
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)


class DeleteView(View):
    key = None
    objecttype = None
    redirect_url = ""
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(self.objecttype, id=kwargs.get(self.key))
        object_name = str(object)
        object.delete()
        messages.add_message(
            request, messages.SUCCESS, f"{object_name} ble slettet", extra_tags="Slettet"
        )
        kwargs.pop(self.key)
        return redirect(reverse(f"cgp:{self.redirect_url}", kwargs=kwargs))
def delete_objects(request, *args, **kwargs):
    object = None
    print(args, kwargs)
    if "country_id" in kwargs.keys():
        object = Country.objects.get(id=kwargs.get("country_id"))
    if request.method == "POST" and object:
        #object.delete()
        #return
        print(1)


    context = {
        "object": object
    }
    return render(request, "cgp/admin/delete.html", context)


