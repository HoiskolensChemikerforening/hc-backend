from django.shortcuts import render
from .models import Candidate, Position, Vote, Position

def index(request):
    positions = print_sorted_candidates(request)
    return render('elections/candidate_list.html',
                              {'position_list':positions})

def print_sorted_candidates(request):
    positions = Position.object.prefetch_related('candidate_set').all()
    return positions
