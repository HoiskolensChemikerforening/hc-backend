from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory

from .models import QuizTerm, QuizScore
from .forms import CreateQuizScoreForm, EditQuizScoreForm, CreateQuizTermForm
from chemie.customprofile.models import Profile

from random import shuffle


def index(request):
    return render(request, "quiz/index.html")


def name_quiz_index(request):
    return render(request, "quiz/name_quiz/index.html")


@login_required
def name_quiz(request, year=1):
    profiles_qs = Profile.objects.filter(grade=year, user__is_active=True)
    profiles = list(profiles_qs)
    profiles_count = profiles_qs.count()
    shuffle(profiles)
    context = {
        "profiles": profiles,
        "profiles_count": profiles_count,
        "year": year,
    }
    return render(request, "quiz/name_quiz/name_quiz.html", context)


def kjellerquiz_index(request):
    try:
        active_term = QuizTerm.objects.get(is_active=True)
        top_scores = active_term.scores.order_by("-score")[:3]
        terms = QuizTerm.objects.exclude(id=active_term.id).order_by("-id")
    except QuizTerm.DoesNotExist:
        active_term = QuizTerm.objects.none()
        top_scores = QuizScore.objects.none()
        terms = QuizTerm.objects.all().order_by("-id")

    context = {
        "active_term": active_term,
        "top_scores": top_scores,
        "terms": terms,
    }

    return render(request, "quiz/kjellerquiz/index.html", context)


@permission_required("quiz.add_quizterm")
def create_term(request):
    form = CreateQuizTermForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("quiz:term_detail", pk=form.instance.pk)

    context = {"form": form}
    return render(request, "quiz/kjellerquiz/create_term.html", context)


@permission_required("quiz.delete_quizterm")
def delete_term(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    term.delete()
    messages.add_message(
        request, messages.SUCCESS, "Quizen ble slettet", extra_tags="Slettet"
    )
    return redirect("quiz:kjellerquiz_index")


@login_required
def term_detail(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = term.scores.order_by("-score")
    context = {"term": term, "scores": scores}
    return render(request, "quiz/kjellerquiz/term_detail.html", context)


@permission_required("quiz.change_quizterm")
def activate_deactivate(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    term.is_active = not term.is_active
    term.save()
    return redirect("quiz:create_score", pk)


@permission_required("quiz.change_quizterm")
def create_score(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = term.scores.order_by("-score")
    form = CreateQuizScoreForm(request.POST or None)

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
        return redirect("quiz:create_score", term.pk)

    context = {"term": term, "scores": scores, "form": form}
    return render(request, "quiz/kjellerquiz/create_score.html", context)


@permission_required("quiz.change_quizscore")
def edit_scores(request, pk):
    term = get_object_or_404(QuizTerm, pk=pk)
    scores = term.scores.order_by("-score")

    MemberFormSet = modelformset_factory(
        QuizScore, form=EditQuizScoreForm, extra=0
    )
    formset = MemberFormSet(request.POST or None, queryset=scores)

    if request.method == "POST":
        if formset.is_valid():
            formset.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Poengene ble lagret",
                extra_tags="Wohoo!",
            )
            return redirect("quiz:create_score", term.pk)

    context = {"term": term, "scores": scores, "formset": formset}

    return render(request, "quiz/kjellerquiz/edit_scores.html", context)
