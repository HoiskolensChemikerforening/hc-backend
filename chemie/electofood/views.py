from django.shortcuts import render, HttpResponse
from django.shortcuts import render
from .models import ElectionQuestionForm, CommiteeAnswer
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    electionform = ElectionQuestionForm.objects.all()[0]
    user = request.user
    committees = electionform.get_participating_committes()
    results = []
    for committe in committees:
        results.append([committe, electionform.calculate_result_commitee(user, committe)])
    context = {
        "title": electionform.title,
        "committees": committees,
        "results": results
    }
    return render(request, "electofeed.html", context)