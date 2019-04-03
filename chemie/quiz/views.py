from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import QuizTerm, QuizScore
from django.contrib import messages
from .forms import QuizScoreForm, CreateQuizTermForm
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.


def index(request):
    try:
        active_term = QuizTerm.objects.get(is_active=True)
        terms = QuizTerm.objects.exclude(id=active_term.id).order_by('id')
    except QuizTerm.DoesNotExist:
        active_term = None
        terms = QuizTerm.objects.all().order_by('id')

    top_scores = QuizScore.objects.filter(term=active_term).order_by('-score')[:3]
    context = {
        "active_term": active_term,
        "top_scores": top_scores,
        "terms": terms
    }

    return render(request, 'quiz/index.html', context)


@permission_required('quiz.add_quizterm')
def create_term(request):
    form = CreateQuizTermForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('quiz:term_detail', pk=form.instance.pk)

    context = {'form': form}
    return render(request, 'quiz/create_term.html', context)


@permission_required("quiz.delete_quizterm")
def delete_term(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    term.delete()
    messages.add_message(
        request, messages.SUCCESS, "Quizen ble slettet", extra_tags="Slettet"
    )
    return redirect('quiz:index')


@login_required
def term_detail(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    context = {
        'term': term,
        'scores': scores
    }
    return render(request, 'quiz/term_detail.html', context)


@permission_required("quiz.change_quizterm")
def activate_deactivate(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    term.is_active = not term.is_active
    term.save()
    return redirect('quiz:create_score', pk)


@permission_required("quiz.change_quizterm")
def create_score(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = QuizScore.objects.filter(term=term).order_by('-score')
    form = QuizScoreForm(request.POST or None)
    activate_form = CreateQuizTermForm(instance=term)
    activate_form.fields.pop('term')
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
        'form': form,
        'activate_form': activate_form
    }
    return render(request, 'quiz/create_score.html', context)


@permission_required('quiz.change_quizscore')
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
