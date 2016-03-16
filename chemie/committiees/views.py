from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from .models import Committee, Person

def index(request):
    committees = print_sorted_persons(request)
    return render_to_response('committees/detail.html', {'Committee_list':committees})

def print_sorted_persons(request):
    # We use prefetch_related to get the related Candidates for each position
    # Even tho position doesn't have any connection to Candidate (its the
    # other way around)
    committees = Committee.objects.prefetch_related('person_set')
    return committees
