from .models import Candidate, Position, Vote, Position
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    positions = print_sorted_candidates(request)
    return render_to_response('elections/detail.html', {'position_list':positions})

def print_sorted_candidates(request):
    # We use prefetch_related to get the related Candidates for each position
    # Even tho position doesn't have any connection to Candidate (its the
    # other way around)
    positions = Position.objects.prefetch_related('candidate_set').filter(active = True)
    return positions
