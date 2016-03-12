from .models import Candidate, Position, Vote, Position, Election, Ticket
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from random import randint
from .forms import Postform


SECRET_CHARS = '23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
TICKET_LENGTH = 8

def index(request):
    positions = print_sorted_candidates(request)
    return render_to_response('elections/detail.html', {'position_list':positions})

def print_sorted_candidates(request):
    # We use prefetch_related to get the related Candidates for each position
    # Even tho position doesn't have any connection to Candidate (its the
    # other way around)
    positions = Position.objects.prefetch_related('candidate_set').filter(active = True)
    return positions


def generate_tickets(ticket_count):
    choices = len(SECRET_CHARS)-1
    chars = range(TICKET_LENGTH)
    count, secret_list, tickets = 0, [], []
    while count < ticket_count:
        secret = [SECRET_CHARS[randint(0,choices)] for x in chars]
        secret_snippet = ''.join(secret)
        if secret not in secret_list:
            secret_list.append(secret_snippet)
            count+= 1

    for secret in secret_list:
        tickets.append(Ticket(secret=secret))

    Ticket.objects.bulk_create(tickets)


def post_votes(request):
    form = Postform()
    context = {
    "form": form,
    }
    return render(request, "post_form.html", context)
