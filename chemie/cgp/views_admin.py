from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import CGP,Group
from .forms import CGPForm, GroupForm, CountryForm
from django.views import View
@permission_required("elections.add_election")
@login_required
def cgp_admin(request):
    cgps = CGP.objects.all()

    if request.method == "POST":  # brukeren trykker på knappen
        CGP.create_new_cgp()


    context = {
        "cgps": cgps,
    }
    return render(request, "cgp/admin/admin.html", context)



@permission_required("elections.add_election")
@login_required
def cgp_edit(request, cgp_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    groups = cgp.group_set.all()


    form = GroupForm()
    context = {
        "cgp": cgp,
        "groups": groups,
        "form":form
    }
    return render(request, "cgp/admin/edit.html", context)

def group_edit(request, cgp_id, group_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    group = get_object_or_404(Group, id=group_id)
    form = GroupForm(instance=group)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.cgp = cgp
            group.has_voted = False
            form.save()
    context = {
        "cgp": cgp,
        "group": group,
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

def group_add(request, cgp_id):
    cgp = get_object_or_404(CGP, id=cgp_id)
    form = GroupForm(request.POST or None)
    if form.is_valid():
        group = form.save(commit=False)
        group.cgp = cgp
        group.has_voted = False
        form.save()

    else:
        form = GroupForm()
    context = {
        "cgp": cgp,
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

def country_edit(request, country_id):
    country = get_object_or_404(Group, id=country_id)
    form = GroupForm(instance=country)

    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            form.save()
    context = {
        "country": country,
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

def country_add(request):
    form = CountryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CountryForm()
    context = {
        "form": form
    }
    return render(request, "cgp/admin/forms.html", context)

