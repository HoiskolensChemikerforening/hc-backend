from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CGP, Country, Group, Vote, POINTS
import json
from .serializers import CGPSerializer
from rest_framework import generics
from django.contrib import messages
from django.db.models.query import QuerySet

@login_required
def index(request):
    """
    Renders the CGP index page. Generates links to the voting pages related to the user if there is an open CGP object.
    Hides those links if not.
    Args:
        request: HttpRequest
    Context:
        countries: set (all countries the request.user can vote for apart from the audience vote)
        audience: Country object or list (the audience country or an empty list if there is none)
        groups: Queryset (all groups the request.user can vote for apart from the audience vote)
        open: boolean (is True if there is an open CGP)
        cgp: cgp (latest active CGP object, latest closed active CGP object if all CGP objects are closed)
    """
    cgp = CGP.get_latest_active()
    if not cgp:
        context = {"cgp": CGP.get_latest_or_create(), "open": False}
        return render(request, "cgp/index.html", context)
    groups = Group.objects.filter(group_leaders__in=[request.user]).filter(cgp=cgp)
    audience = list(Group.objects.filter(audience=True, cgp=cgp))
    if len(audience) > 0:
        audience = [audience[0].country]
    countries = set([group.country for group in groups])
    context = {"countries": countries,
               "audience": audience,
               "groups": groups,
               "open": True,
               "cgp": cgp}

    return render(request, "cgp/index.html", context)


def check_group_access(request, group, manage=False):
    """
    Checks if a person has permissions to submit votes for this group.
    Args:
        request: HttpRequest
        group: Group
        manage: boolean (switch between group members and leaders)
    """
    if group.audience:
        return True
    if manage:
        permittedUsersLst = group.group_leaders.all()
    else:
        permittedUsersLst = group.group_members.all()
    if request.user not in permittedUsersLst:
        return False
    return True


@login_required
def vote_index(request, slug):
    """
    Renders the voting page for a country.
    Args:
        request: HttpRequest
        slug: str (slugified countryname)
    Context:
        country: Country (current Country object)
        groups: Queryset (containing all Group objects that can be voted for by the current Group object)
        countries: str (containing all country names that can be voted for by the current Group object seperated by ",")
        realnames: str (containing all group names that can be voted for by the current Group object seperated by ",")
        songtiteles: str (containing all songtitles that can be voted for by the current Group object seperated by ",")
        points: str (containing all points that can be assigned to Group objects seperated by ",")
        failure_group: Group (Group object from a previous vote)
        show_group: Group (Group object from a previous vote)
    """
    country = get_object_or_404(Country, slug=slug)
    group = get_object_or_404(Group, country=country, cgp=CGP.get_latest_active())
    if not check_group_access(request, group, manage=True):
        return redirect('/cgp')
    cgp = CGP.get_latest_active()

    #sort group by previous votes or random
    vote_set = group.vote_set.filter(final_vote=True)
    groups = cgp.group_set.exclude(id=group.id).exclude(audience=True).order_by('?')
    failure_group, show_group= None, None
    if len(vote_set) >= 1:
        groups, failure_group, show_group = vote_set[0].get_sorted_groups_list()
    elif group.audience:
        user_vote_set = group.vote_set.filter(user=request.user)
        if len(user_vote_set) >= 1:
            groups, failure_group, show_group = user_vote_set[0].get_sorted_groups_list()


    points = POINTS
    if request.method == "POST":
        if not request.POST.get("showprize") or not request.POST.get("failureprise"):
            return JsonResponse({}, status=422)
        countryNames = request.POST.getlist("countryNames[]")
        showprize = Group.objects.get(id=request.POST.get("showprize"))
        failureprize = Group.objects.get(id=request.POST.get("failureprise"))
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
            request, messages.SUCCESS, f"Takk for at du bruker stemmen din! Dersom du ønsker å redigere stemmen din kan du stemme på nytt så lenge valget er åpent.", extra_tags="Stemme registrert"
        )
        return JsonResponse({"url": reverse("cgp:index")}, status=200)

    context = {
        "country": country,
        "groups": groups,
        "countries": ",".join([i.country.country_name for i in groups]),
        "realnames": ",".join([i.real_name for i in groups]),
        "songtiteles": ",".join([i.song_name for i in groups]),
        "points": ",".join([str(i) for i in points]),
        "failure_group": failure_group,
        "show_group": show_group,
               }
    return render(request, "cgp/vote_index.html", context)




#API views
class CGPListViewTemplate(generics.ListCreateAPIView):
    """
    Renders the CGP API page. Populates it with all final votes.
    Data:
         queryset: Queryset (All final votes related to the latest active CGP object)
    """

    queryset = Vote.objects.none()
    serializer_class = CGPSerializer
    def get_queryset(self):
        """
        overrides the original get_queryset method to exclude votes not related to the latest CGP
        """
        queryset = super().get_queryset()
        if isinstance(queryset, QuerySet):
            cgp = CGP.get_latest_or_create()
            queryset = Vote.objects.filter(group__cgp=cgp).exclude(final_vote=False)
        return queryset

