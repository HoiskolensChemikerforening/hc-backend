from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country, Group, Vote, POINTS
import json
from .serializers import CGPSerializer
from rest_framework import generics
from django.contrib import messages



#bugs
#Hva skjer når CGP ikke finnes


@login_required
def index(request):
    cgp = CGP.get_latest_active()
    if not cgp:
        context = {"cgp": CGP.get_latest_or_create(),"open":False}
        return render(request, "cgp/index.html", context)
    groups = Group.objects.filter(group_leaders__in=[request.user]).filter(cgp=cgp)
    audience = list(Group.objects.filter(audience=True, cgp=cgp))
    if len(audience) > 0:
        audience = [audience[0].country]
    countries = set([group.country for group in groups])#+audience)
    context = {"countries": countries,
               "audience": audience,
               "groups": groups,
               "open":True,
               "cgp": cgp}

    return render(request, "cgp/index.html", context)


def check_group_access(request, group, manage=False):
    if group.audience:
        return True
    if manage:
        permittedUsersLst = group.group_leaders.all()
    else:
        permittedUsersLst = group.group_members.all()
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
    groups = cgp.group_set.exclude(id=group.id).exclude(audience=True)
    points = POINTS
    if request.method == "POST":
        if not request.POST.get("showprize") or not request.POST.get("failureprise"):
            return JsonResponse({}, status=422)
        countryNames = request.POST.getlist("countryNames[]")
        showprize = Group.objects.get(id=request.POST.get("showprize"))
        failureprize = Group.objects.get(id=request.POST.get("failureprise"))
        #if finalvote
            #if finalvote for group exists
            #else
        #else:
            #if vote for group and person exists
            #else
        if group.audience:
            if len(group.vote_set.filter(user=request.user).filter(final_vote=False)) > 0:
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
        vote.showprize_vote = showprize
        vote.failureprize_vote = failureprize
        vote.user = request.user
        vote.save()
        messages.add_message(
            request, messages.SUCCESS, f"Takk for at du bruker stemmen din!", extra_tags="Stemme registrert"
        )
        return JsonResponse({"url": reverse("cgp:index")}, status=200)
        #return redirect(reverse("cgp:vote_show_index", args=[slug]))

    #sort groups after current vote or random
    context = {
        "country": country,
        "group": group,
        "groups": groups,
        "countries": ",".join([i.country.country_name for i in groups]),
        "realnames": ",".join([i.real_name for i in groups]),
        "songtiteles": ",".join([i.song_name for i in groups]),
        "points": ",".join([str(i) for i in points]),
        "url": f"/{slug}/"
               }
    return render(request, "cgp/vote_index.html", context)





#API views
class CGPListViewTemplate(generics.ListCreateAPIView):
    cgp = CGP.get_latest_active()
    queryset = Vote.objects.filter(group__cgp=cgp).exclude(final_vote=False)
    serializer_class = CGPSerializer
