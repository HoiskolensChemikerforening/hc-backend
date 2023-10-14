from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ElectionQuestionForm, CommiteeAnswer, VALUES,UserAnswer, ElectionQuestion
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AnswerForm, ElectionQuestionFormForm, ElectionQuestionCreateForm
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

def get_committee_and_answer(request, electionform, committee_id):
    if not committee_id:
        answers = UserAnswer.objects.filter(user=request.user).filter(question__question_form=electionform)
        committee = None
    else:
        answers = CommiteeAnswer.objects.filter(committee__id=committee_id).filter(question__question_form=electionform)
        committee = get_object_or_404(Committee, id=committee_id)
    return answers, committee
@login_required()
def valgomat_form(request, id, committee_id=None):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    print(electionform)
    questions = electionform.electionquestion_set.all()

    answers, committee = get_committee_and_answer(request, electionform, committee_id)
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
        "committee": committee,
        "electionform": electionform
    }
    return render(request, "electofeedform.html", context)

@login_required()
def valgomat_result(request, id):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    questions = electionform.electionquestion_set.all()
    committees = electionform.get_participating_committes()
    results = []
    colors = COLORS
    random.shuffle(colors)
    for i, committe in enumerate(committees):
        results.append([committe, electionform.calculate_result_commitee(request.user, committe), colors[(i%len(colors))]])
    results.sort(key=lambda x: x[1], reverse=True)

    questionvalueanswerslist = []

    for question in questions:
        questionlst = []
        for value in VALUES:
            committee_answer = CommiteeAnswer.objects.filter(question=question).filter(answer=value[0])
            user_answer = UserAnswer.objects.filter(question=question).filter(answer=value[0]).filter(user=request.user)
            merged_list = [user.get_name() for user in user_answer]+[committee.get_name() for committee in committee_answer]
            questionlst.append((value, merged_list))
        questionvalueanswerslist.append((question,questionlst))

    context = {
        "results": results,
        "questions": questions,
        "values": VALUES,
        "questionvalueanswerslist": questionvalueanswerslist,
        "electionform": electionform
    }
    return render(request, "electofeedresults.html", context)



@permission_required("electofood.change_electionquestionform")
def create_valgomat(request):
    form = ElectionQuestionFormForm(request.POST or None)
    print(form.is_valid(), form, request.POST, request)
    if request.POST and form.is_valid():
        valgomat = form.save()
        print("hi")
        return redirect(reverse("valgomat:valgomat_rediger", kwargs={"id": valgomat.id}))

    context = {
        "form": form
    }
    return render(request, "createvalgomat.html", context)


@permission_required("electofood.change_electionquestionform")
def edit_valgomat(request, id):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    form = ElectionQuestionCreateForm(request.POST or None)



    if request.POST and form.is_valid():
        question = form.save(commit=False)
        question.question_form = electionform
        question.save()

    questions = electionform.electionquestion_set.all()
    form = ElectionQuestionCreateForm(None)
    context = {
        "form": form,
        "electionform": electionform,
        "questions":questions
    }


    return render(request, "editvalgomat.html", context)

@permission_required("electofood.change_electionquestionform")
def delete_question(request, id, question_id):
    question = get_object_or_404(ElectionQuestion, id=question_id)
    question.delete()


    return redirect(reverse("valgomat:valgomat_rediger", kwargs={"id": id}))


@permission_required("electofood.change_electionquestionform")
def delete_valgomat(request, id, valgomat_id):
    electionform = get_object_or_404(ElectionQuestionForm, id=valgomat_id)
    electionform.delete()


    return redirect(reverse("valgomat:index_valgomat"))



