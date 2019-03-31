from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QuizTerm, QuizScore
from .forms import QuizScoreForm, CreateQuizTermForm
# Create your views here.


def index(request):
    return HttpResponse("Hei <3")


def create_term(request):
    form = CreateQuizTermForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('quiz:term_detail', pk=form.instance.pk)

    context = {'form': form}
    return render(request, 'quiz/create_term.html', context)


def term_detail(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    context = {
        'term': term,
        'scores': scores
    }
    return render(request, 'quiz/term_detail.html', context)


def create_score(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    form = QuizScoreForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            if scores.filter(user=instance.user):
                # Oppdater eksisterende score fremfor å legge til ny
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


def edit_score(request, pk):
    quiz_score_edit = get_object_or_404(QuizScore, pk=pk)
    term = quiz_score_edit.term
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    form = QuizScoreForm(request.POST or None)
    form.fields.pop('user')
    if form.is_valid():
        instance = form.save(commit=False)
        quiz_score_edit.score += instance.score
        quiz_score_edit.save()
        return redirect('quiz:create_score', term.pk)
    context = {
        'term': term,
        'scores': scores,
        'form': form,
        'quiz_score_edit': quiz_score_edit
    }
    return render(request, 'quiz/create_score.html', context)
