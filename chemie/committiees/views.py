from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from .models import Committee, Member

def index(request):
    committees = Committee.objects.all()
    members = Member.objects.all()
    context = {
        'committees': committees,
        'members': members,
    }

    return render_to_response('committees/detail.html',context)
