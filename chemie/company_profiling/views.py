from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from .models import Company, Position, Interview


def ListCompanies(request):
    company = get_object_or_404(Company)

    context = {
        'company': company
    }
    return context


def ListPositions(request):
    position = get_object_or_404(Position)

    context = {
        'position': position
    }
    return context


def ListInterviews(request):
    interview = get_object_or_404(Interview)

    context = {
        'interview': interview
    }
    return context

