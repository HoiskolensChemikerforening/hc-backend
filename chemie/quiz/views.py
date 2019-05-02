from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QuizTerm, QuizScore
from .forms import QuizScoreForm
# Create your views here.


def index(request):
    return HttpResponse("Hei <3")


def term_detail(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    context = {
        'term': term,
        'scores': scores
    }
    return render(request, 'quiz/term_detail.html', context)


def create_score(request, pk):
    # TODO: Fix responsive dal widget (and responsive table?)
    # TODO: Create option to update existing scores

    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    form = QuizScoreForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            if scores.filter(user=instance.user):
                # Oppdater eksisterende fremfor å legge til ny
                quiz_score = scores.filter(user=instance.user).first()
                quiz_score.score += instance.score
                quiz_score.save()
            else:
                instance.term = term
                instance.save()
            return redirect('quiz:create_score', term.pk)
    context = {
        'term': term,
        'scores': scores,
        'form': form
    }
    return render(request, 'quiz/create_score.html', context)
