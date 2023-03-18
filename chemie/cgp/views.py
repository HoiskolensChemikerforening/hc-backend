from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country, CgpPosition, Group, Vote
import json

#bugs
#Hva skjer når CGP ikke finnes


@login_required
def index(request):
    cgp = CGP.get_latest_active()
    positions = CgpPosition.objects.filter(users=request.user).filter(group__cgp=cgp)
    countries = set([p.group.country for p in positions])
    context = {"countries": countries}

    return render(request, "cgp/index.html", context)


def check_group_access(request, group, manage=False):
    permittedUsersLst = []
    if manage:
        for p in group.cgpposition_set.filter(can_manage_country=True):
            permittedUsersLst = permittedUsersLst + list(p.users.all())
    else:
        for p in group.cgpposition_set.all():
            permittedUsersLst = permittedUsersLst + list(p.users.all())
    if request.user not in permittedUsersLst:
        return False
    return True

def vote_index(request, slug):
    country = get_object_or_404(Country, slug=slug)
    group = country.group_set.filter(cgp=CGP.get_latest_active())
    if len(group)>1:
        print("2 groups are part of the same country")
    group = group[0]
    if not check_group_access(request, group, manage=True):
        return redirect('/cgp')
    cgp = CGP.get_latest_active()
    #countries = ",".join([i.country.country_name for i in cgp.group_set.all()]),#[g.country for g in cgp.group_set.all()]
    groups = cgp.group_set.exclude(group_username=group.group_username)
    points = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
    if request.method == "POST":
        countryNames = request.POST.getlist("countryNames[]")

        #if finalvote
            #if finalvote for group exists
            #else
        #else:
            #if vote for group and person exists
            #else
        if len(group.vote_set.filter(final_vote=True)) > 0:
            vote = group.vote_set.all()[0]
        else:
            vote = Vote()
            vote.final_vote = True
            vote.group = group
        vote.vote = json.dumps(countryNames)
        vote.user = request.user
        vote.save()
        return JsonResponse({"url": reverse("cgp:index")}, status=200)

    context = {
        "country": country,
        "group": group,
        "countries": ",".join([i.country.country_name for i in groups]),
        "realnames": ",".join([i.real_name for i in groups]),
        "songtiteles": ",".join([i.song_name for i in groups]),
        "points": ",".join([str(i) for i in points]),
        "url": f"/{slug}/"
               }
    return render(request, "cgp/vote_index.html", context)