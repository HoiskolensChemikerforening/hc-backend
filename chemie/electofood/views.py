from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ElectionQuestionForm, CommiteeAnswer, VALUES,UserAnswer
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm
from django.urls import reverse
import random


from django.template.defaulttags import register

COLORS = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def index(request):
    electionform = ElectionQuestionForm.objects.all()[0]
    user = request.user
    committees = electionform.get_participating_committes()
    dissagreement = electionform.get_max_disagreement_sum()
    results = []
    for committe in committees:
        results.append([committe, electionform.calculate_result_commitee(user, committe)])
    context = {
        "title": electionform.title,
        "results": results,
        "dissagreement": dissagreement
    }
    return render(request, "electofeed.html", context)


@login_required()
def valgomat_form(request, id, committe_id=None):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    questions = electionform.electionquestion_set.all()

    if not committe_id:
        answers = UserAnswer.objects.filter(user=request.user).filter(question__question_form=electionform)
        committee = None
    else:
        answers = CommiteeAnswer.objects.filter(committee__id=committe_id).filter(question__question_form=electionform)
        committee = get_object_or_404(Committee, id=committe_id)
    answer_dict = None
    if len(answers) == len(questions):
        answer_dict = {}
        for answer in answers:
            answer_dict[answer.question.id] = answer.answer

    if request.POST:
        valid = True
        for question in questions:
            if str(question.id) not in request.POST.keys():
                valid = False
        if valid:
            if not answer_dict:
                for question in questions:
                    if not committe_id:
                        answer = UserAnswer()
                        answer.user = request.user
                    else:
                        answer = CommiteeAnswer()
                        answer.committee = committee
                    answer.question = question
                    answer.answer = int(request.POST[str(question.id)])
                    answer.save()
                return redirect(reverse("valgomat:valgomat_result", kwargs={"id": id}))
            else:
                for answer in answers:
                    answer.answer = int(request.POST[str(answer.question.id)])
                    answer.save()
                return redirect(reverse("valgomat:valgomat_result", kwargs={"id": id}))





    context = {
        "questions": questions,
        "values": VALUES,
        "answer_dict": answer_dict
    }
    return render(request, "electofeedform.html", context)


@login_required()
def valgomat_result(request, id):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    committees = electionform.get_participating_committes()
    results = []
    colors = COLORS
    random.shuffle(colors)
    for i, committe in enumerate(committees):
        results.append([committe, electionform.calculate_result_commitee(request.user, committe),colors[(i%len(colors))]])
    results.sort(key=lambda x: x[1], reverse=True)
    context={
        "results": results,
    }
    return render(request, "electofeedresults.html", context)