from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QuizTerm, QuizScore
# Create your views here.


def index(request):
    return HttpResponse("Hei <3")


def quiz_term(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    context = {
        'term': term,
        'scores': scores
    }
    return render(request, 'quiz/term_detail.html', context)
