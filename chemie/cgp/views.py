from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country, CgpPosition, Group, Vote
import json
from rest_framework.views import APIView
from .serializers import CGPSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

POINTS = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
#bugs
#Hva skjer når CGP ikke finnes


@login_required
def index(request):
    cgp = CGP.get_latest_active()
    positions = CgpPosition.objects.filter(users=request.user).filter(group__cgp=cgp)
    audience = list(Group.objects.filter(group_username="publikum", cgp=cgp))
    if len(audience) > 0:
        audience = [audience[0].country]
    countries = set([p.group.country for p in positions]+audience)
    context = {"countries": countries,
               "audience": audience}

    return render(request, "cgp/index.html", context)


def check_group_access(request, group, manage=False):
    permittedUsersLst = []
    if group.group_username == "publikum":
        return True
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
    print(group.group_username == "publikum")
    if not check_group_access(request, group, manage=True):
        return redirect('/cgp')
    cgp = CGP.get_latest_active()
    #countries = ",".join([i.country.country_name for i in cgp.group_set.all()]),#[g.country for g in cgp.group_set.all()]
    groups = cgp.group_set.exclude(group_username=group.group_username)
    points = POINTS
    if request.method == "POST":
        countryNames = request.POST.getlist("countryNames[]")

        #if finalvote
            #if finalvote for group exists
            #else
        #else:
            #if vote for group and person exists
            #else
        if group.group_username == "publikum":
            if len(group.vote_set.filter(user=request.user)) > 0:
                vote = group.vote_set.filter(user=request.user)[0]
            else:
                vote = Vote()
                vote.final_vote = False
                vote.group = group
        else:
            if len(group.vote_set.filter(final_vote=True)) > 0:
                vote = group.vote_set.filter(final_vote=True)[0]
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


class CGPListViewTemplate(generics.ListCreateAPIView):
    cgp = CGP.get_latest_active()
    audience_groups = Group.objects.filter(cgp=cgp).filter(group_username="publikum")

    if len(audience_groups)>0:
        audience_group = audience_groups[0]
        audience_votes = audience_group.vote_set.all()

        if len(audience_votes.filter(final_vote=True))>0:
            final_audience_vote = audience_votes.filter(final_vote=True)[0]
        else:
            final_audience_vote = Vote()
            final_audience_vote.final_vote = True
            final_audience_vote.group = audience_group
        #final_audience_vote.user = request.user
        vote_dict = {}
        for vote in audience_votes.filter(final_vote=False):
            for count, country in enumerate(vote.vote.replace("]", "").replace("[", "").replace("\"", "").split(",")):
                if count >= len(POINTS):
                    break
                if country in vote_dict.keys():
                    vote_dict[country] += POINTS[count]
                else:
                    vote_dict[country] = POINTS[count]
        print(vote_dict)
        print(",".join([i[0] for i in sorted(vote_dict.items(), key=lambda item: item[1], reverse=True)]))


        #final_audience_vote.vote =

    queryset = Vote.objects.filter(group__cgp=cgp).exclude(final_vote=False)
    serializer_class = CGPSerializer
