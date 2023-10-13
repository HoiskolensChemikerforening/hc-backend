from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import ElectionQuestionForm, CommiteeAnswer, VALUES,UserAnswer
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm


from django.template.defaulttags import register

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
def valgomat_form(request, id):
    electionform = get_object_or_404(ElectionQuestionForm, id=id)
    questions = electionform.electionquestion_set.all()

    #print([question.answer_set.filter(useranswer__user=request.user) for question in questions])
    user_answers = UserAnswer.objects.filter(user=request.user).filter(question__question_form=electionform)
    answer_dict = None
    if len(user_answers) == len(questions):
        answer_dict = {}
        for user_answer in user_answers:
            answer_dict[user_answer.question.id]=user_answer.answer



    if request.POST:
        valid = True
        for question in questions:
            if str(question.id) not in request.POST.keys():
                valid = False
        print(valid)






    print(answer_dict)
    context = {
        "questions": questions,
        "values": VALUES,
        "answer_dict":answer_dict
    }
    return render(request, "electofeedform.html", context)