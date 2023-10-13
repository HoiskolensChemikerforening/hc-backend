from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import ElectionQuestionForm, CommiteeAnswer, VALUES
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm


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
    form = AnswerForm(request.POST or None)
    if request.POST:
        valid = True
        for question in questions:
            if str(question.id) not in request.POST.keys():
                valid = False
        print(valid)







    context = {
        "questions": questions,
        "values": VALUES,
        "form": form
    }
    return render(request, "electofeedform.html", context)