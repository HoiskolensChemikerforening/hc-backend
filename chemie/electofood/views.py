from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    ElectionQuestionForm,
    CommiteeAnswer,
    VALUES,
    UserAnswer,
    ElectionQuestion,
)
from chemie.committees.models import Committee
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ElectionQuestionFormForm, ElectionQuestionCreateForm
from django.urls import reverse
import random
from django.contrib import messages

from django.template.defaulttags import register

#Colors to visualize the percentage bars
COLORS = [
    "#ea5545",
    "#f46a9b",
    "#ef9b20",
    "#edbf33",
    "#ede15b",
    "#bdcf32",
    "#87bc45",
    "#27aeef",
    "#b33dc6",
]


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary. Used in django templates as a filter.
    Args:
        dictionary: dict (Python dictionary)
        key: key contained in dictionary
    returns:
        value
    """
    return dictionary.get(key)


@login_required
def index(request):
    """
    Renders the valgomat index page.
    Args:
        request (Http request)
    returns
        rendered html
    """
    #Get all valgomat objects
    electionforms = ElectionQuestionForm.objects.all()

    #Get the current user
    user = request.user

    #Get all committees the user is a part of
    committees = Committee.objects.filter(position__users=user).distinct()

    #Render HTML
    context = {"electionforms": electionforms, "committees": committees}
    return render(request, "electofeed.html", context)


def get_committee_and_answer(request, electionform, committee_id):
    """
    Get all answer objects related to the electionform and the current user or committee based on the committee_id.
    Args:
        request: Http request
        electionform: ElectionQuestionForm object
        committee_id: int (id of a existing committee)
    returns:
        answers: all related answer objects (UserAnswer or CommiteeAnswer)
        committee: related committee or None
    """

    #Check if we should return UserAnswer or CommiteeAnswer objects
    if not committee_id:
        # Get all related UserAnswer objects
        answers = UserAnswer.objects.filter(user=request.user).filter(
            question__question_form=electionform
        )
        committee = None
    else:
        # Get all related CommiteeAnswer objects
        answers = CommiteeAnswer.objects.filter(
            committee__id=committee_id
        ).filter(question__question_form=electionform)

        # Populate the committee variable
        committee = get_object_or_404(Committee, id=committee_id)
    return answers, committee


def delete_old_answers(old_answers):
    """
    Deletes old answers to prevent the existence of 2 answers for the same question submittet by the same person or committee.
    Args:
        old_answers: answers to be deleted
    returns:
        None
    """
    #Check if old answers exist
    if len(old_answers) > 0:
        # Iterate through old answers and delete.
        for answer in old_answers:
            answer.delete()
    return


@login_required()
def valgomat_form(request, id, committee_id=None):
    """
    Renders the valgomat form page.
    Args:
        request: Html request
        id: int (id of an ElectionQuestionForm object)
        committee_id: int (id of a Committee object)
    """

    # Get valgomat object
    electionform = get_object_or_404(ElectionQuestionForm, id=id)

    # Fetch all questions related to the currently selectet valgomat.
    questions = electionform.electionquestion_set.all()

    # Fetch all answers and the committee if applicable
    answers, committee = get_committee_and_answer(
        request, electionform, committee_id
    )



    answer_dict = None
    # Check if previous answers exist
    if len(answers) == len(questions):
        # Create a dictionary containing question id's and the users/committees previous answers
        answer_dict = {}
        for answer in answers:
            answer_dict[answer.question.id] = answer.answer


    if request.POST:
        # Check if the form is valid.
        valid = True
        for question in questions:
            if str(question.id) not in request.POST.keys():
                valid = False
        if valid:
            # Initialize variable to check if all answers have been saved
            saved = False

            # Check if there are NO previous answers to all questions
            if not answer_dict:
                # Iterate through all questions
                for question in questions:
                    if not committee_id:
                        # Delete all previous answers saved for the current question by the current user
                        old_answers = question.answer_set.filter(
                            useranswer__user=request.user
                        )
                        delete_old_answers(old_answers)

                        # Create a new answer
                        answer = UserAnswer()
                        answer.user = request.user
                    else:
                        # Delete all previous answers saved for the current question by the current committee
                        old_answers = question.answer_set.filter(
                            commiteeanswer__committee=committee
                        )
                        delete_old_answers(old_answers)

                        # Create a new answer
                        answer = CommiteeAnswer()
                        answer.committee = committee

                    # Populate the answer object with data and save
                    answer.question = question
                    answer.answer = int(request.POST[str(question.id)])
                    answer.save()
                saved = True
            else:
                # Iterate through all answers
                for answer in answers:
                    # Update and save answer
                    answer.answer = int(request.POST[str(answer.question.id)])
                    answer.save()
                saved = True

            # Redirect if saved
            if saved:
                # Redirect to result page for a single user
                if not committee_id:
                    return redirect(
                        reverse("valgomat:valgomat_result", kwargs={"id": id})
                    )
                else:
                    # Redirect to index page for a committee
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"Valgomat svaret for {committee} har blitt redigert.",
                        extra_tags="Takk!",
                    )
                    return redirect(reverse("valgomat:index_valgomat"))

    #Render page
    context = {
        "questions": questions,
        "values": VALUES,
        "answer_dict": answer_dict,
        "committee": committee,
        "electionform": electionform,
    }
    return render(request, "electofeedform.html", context)


@login_required()
def valgomat_result(request, id):
    """
    Renders the result page of the valgomat.
    Args:
        request: Html request
        id: int (id if the ElectionQuestionForm)
    return:
        html reponse
    """

    # Fetch the currently selectet ElectionQuestionForm object by id
    electionform = get_object_or_404(ElectionQuestionForm, id=id)

    # Fetch all corresponding questions
    questions = electionform.electionquestion_set.all()

    # Fetch all committees which have submittet an answer
    committees = electionform.get_participating_committes()

    #Initialize a list to contain the result
    results = []

    # Fetch colors and reshuffle them
    colors = COLORS
    random.shuffle(colors)

    # Iterate through all participation committees
    for i, committe in enumerate(committees):
        # Append committee, result in %, and color to result list
        results.append(
            [
                committe,
                electionform.calculate_result_commitee(request.user, committe),
                colors[(i % len(colors))],
            ]
        )

    # Sort result list by percentage (decending)
    results.sort(key=lambda x: x[1], reverse=True)

    # Initialize list to contain the answers of all committees and the current user for all questions
    # [(question, [(value, [user, committee1, committe2, ...]), ...]), ...]
    questionvalueanswerslist = []

    # Iterate through all questions
    for question in questions:
        questionlst = []
        # Iterate through all alternatives
        for value in VALUES:

            # Fetch the all committee answers which picked the current alternative as an answer
            committee_answer = CommiteeAnswer.objects.filter(
                question=question
            ).filter(answer=value[0])

            # Fetch the user answer of the current user if the user picked the current alternative as an answer
            user_answer = (
                UserAnswer.objects.filter(question=question)
                .filter(answer=value[0])
                .filter(user=request.user)
            )

            # Merge both answer list and convert Answer objects to a readable string
            merged_list = [user.get_name() for user in user_answer] + [
                committee.get_name() for committee in committee_answer
            ]

            #Append the lists to create the questionvalueanswerslist
            questionlst.append((value, merged_list))
        questionvalueanswerslist.append((question, questionlst))

    context = {
        "results": results,
        "questions": questions,
        "values": VALUES,
        "questionvalueanswerslist": questionvalueanswerslist,
        "electionform": electionform,
    }
    return render(request, "electofeedresults.html", context)


@permission_required("electofood.change_electionquestionform")
def create_valgomat(request, id=None):
    """
    Create a new ElectionQuestionForm or edit a ElectionQuestionForm object.
    Args:
        request: html request
        id: int or None (id of a ElectionQuestionForm object to be edited. None if a new ElectionQuestionForm should be created.)
    returns:
        renders html
    """

    # Check if a ElectionQuestionForm should be edited
    if id:
        # Fetch ElectionQuestionForm to edit and populate form
        electform = get_object_or_404(ElectionQuestionForm, id=id)
        form = ElectionQuestionFormForm(instance=electform)
    else:
        # Create emtpty form
        form = ElectionQuestionFormForm(None)

    if request.POST:
        # Check if a ElectionQuestionForm should be edited
        if id:
            # Populate form with POST data
            form = ElectionQuestionFormForm(request.POST, instance=electform)
        else:
            # Populate form with POST data
            form = ElectionQuestionFormForm(request.POST)

        # Validate form
        if form.is_valid():
            # Save form and redirect to change questions page
            valgomat = form.save()
            return redirect(
                reverse(
                    "valgomat:valgomat_rediger", kwargs={"id": valgomat.id}
                )
            )

    # Render page
    context = {"form": form, "id": id}
    return render(request, "createvalgomat.html", context)


@permission_required("electofood.change_electionquestionform")
def edit_valgomat(request, id):
    """
    Edit ElectionQuestion objects related to a valgomat.
    Args:
        request: Http request
        id: int (ElectionQuestionForm id)
    returns:
        renders html
    """

    # Fetch currently selected ElectionQuestionForm
    electionform = get_object_or_404(ElectionQuestionForm, id=id)

    # Initialize ElectionQuestion form
    form = ElectionQuestionCreateForm(request.POST or None)

    # Validate form and save new ElectionQuestion
    if request.POST and form.is_valid():
        question = form.save(commit=False)
        question.question_form = electionform
        question.save()

    # Fetch all corresponding questions
    questions = electionform.electionquestion_set.all()

    # Clear form content
    form = ElectionQuestionCreateForm(None)

    # Render page
    context = {
        "form": form,
        "electionform": electionform,
        "questions": questions,
    }

    return render(request, "editvalgomat.html", context)


@permission_required("electofood.change_electionquestionform")
def delete_question(request, id, question_id):
    """
    Delete a ElectionQuestion object.
    Args:
        id: int (ElectionQuestionForm id)
        question_id: int (ElectionQuestion id)
    returns:
        redirects to edit valgomat page
    """

    # Fetch question to delete
    question = get_object_or_404(ElectionQuestion, id=question_id)

    # Delete ElectionQuestion
    question.delete()

    # Redirect
    return redirect(reverse("valgomat:valgomat_rediger", kwargs={"id": id}))


@permission_required("electofood.change_electionquestionform")
def delete_valgomat(request, id):
    """
        Delete a ElectionQuestionForm object.
        Args:
            id: int (ElectionQuestionForm id)
        returns:
            redirects to edit index page
        """

    # Fetch valgomat form
    electionform = get_object_or_404(ElectionQuestionForm, id=id)

    # Delete ElectionQuestionForm object
    electionform.delete()

    # Redirect to index
    return redirect(reverse("valgomat:index_valgomat"))
