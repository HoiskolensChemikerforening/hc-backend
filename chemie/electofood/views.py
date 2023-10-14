from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ElectionQuestionForm, CommiteeAnswer, VALUES,UserAnswer
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm
from django.urls import reverse
import random
from django.contrib import messages

from django.template.defaulttags import register

COLORS = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def index(request):
    electionforms = ElectionQuestionForm.objects.all()
    user = request.user
    committees = Committee.objects.filter(position__users=user)

    context = {
        "electionforms": electionforms,
        "committees": committees
    }
    return render(request, "electofeed.html", context)


@login_required()
def valgomat_form(request, id, committee_id=None):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    questions = electionform.electionquestion_set.all()

    if not committee_id:
        answers = UserAnswer.objects.filter(user=request.user).filter(question__question_form=electionform)
        committee = None
    else:
        answers = CommiteeAnswer.objects.filter(committee__id=committee_id).filter(question__question_form=electionform)
        committee = get_object_or_404(Committee, id=committee_id)
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
                    if not committee_id:
                        answer = UserAnswer()
                        answer.user = request.user
                    else:
                        answer = CommiteeAnswer()
                        answer.committee = committee
                    answer.question = question
                    answer.answer = int(request.POST[str(question.id)])
                    answer.save()
                if not committee_id:
                    return redirect(reverse("valgomat:valgomat_result", kwargs={"id": id}))
                else:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"Valgomat svaret for {committee} har blitt registrert.",
                        extra_tags="Takk!",
                    )
                    return redirect(reverse("valgomat:index_valgomat"))
            else:
                for answer in answers:
                    answer.answer = int(request.POST[str(answer.question.id)])
                    answer.save()
                if not committee_id:
                    return redirect(reverse("valgomat:valgomat_result", kwargs={"id": id}))
                else:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"Valgomat svaret for {committee} har blitt redigert.",
                        extra_tags="Takk!",
                    )
                    return redirect(reverse("valgomat:index_valgomat"))





    context = {
        "questions": questions,
        "values": VALUES,
        "answer_dict": answer_dict,
        "committee":committee
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