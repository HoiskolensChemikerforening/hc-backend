from django.db import models
from chemie.committees.models import Committee
from django.contrib.auth.models import User


# Alternatives to pick from when using the valgomat
VALUES = (
    (-3, "Helt uenig"),
    (-2, "Litt uenig"),
    (2, "Litt enig"),
    (3, "Helt enig"),
)


class ElectionQuestionForm(models.Model):
    """
    Model to store the data of a single valgomat question set.
    Fields:
        title: str (Valgomat title)
        description: str (Valgomat description)
        active: boolean (Track if the valgomat is active)
    Related:
        electionquestion_set: queryset containing all related questions.
    """

    title = models.CharField(max_length=40, verbose_name="Tittel")
    description = models.TextField(
        max_length=300, default="", verbose_name="Beskrivelse"
    )
    active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        """
        Returns the object name.
        returns:
            title: str (object title)
        """
        return self.title

    def calculate_result_commitee(self, user, committee):
        """
        Calculates the similarity between the user and a committee in percent.
        Args:
            user: User object (user using the valgomat)
            committee: Committee object (Committee to compare with the user)
        Returns:
            percent_agreement: int (Agreement percentage between 0-100)
        """

        # Initialize disagreement value
        disagreement_sum = 0

        # Iterate through all related questions
        for question in self.electionquestion_set.all():
            # Fetch the user answer (as queryset containing 1 object)
            answer = question.answer_set.filter(useranswer__user=user)
            # Fetch committee answer (as queryset containing 1 object)
            commitee_answer = question.answer_set.filter(
                commiteeanswer__committee=committee
            )

            # Add the absolute value of the numerical difference to the disagreementsum
            disagreement_sum += abs(
                answer[0].answer - commitee_answer[0].answer
            )

        # Fetch the maximum disagreement value to calculate a disagreement percentage
        max_disagreement_sum = self.get_max_disagreement_sum()

        # Return agreement percentage (100 - disagreement percentage)
        return int((1 - (disagreement_sum / max_disagreement_sum)) * 100)

    def get_participating_committes(self):
        """
        Fetch all committees with an answer to EVERY question in the current ElectionQuestionForm object.
        Returns:
            committees: list (list containing all committees with answers to every question)
        """

        # Initialize committees list
        committes = []

        # Iterate through all committees
        for committe in Committee.objects.all():
            # Check if the committee has submitted at least one answer to every question related to the ElectionQuestionForm
            if not 0 in [
                len(q.answer_set.filter(commiteeanswer__committee=committe))
                for q in self.electionquestion_set.all()
            ]:
                # Append committee
                committes.append(committe)
        return committes

    def get_max_disagreement_sum(self):
        """
        Get the maximum disagreement sum.
        Return:
            max_disagreement_sum: int (Maximum dissagreement sum)
        """

        # Get the amount of questions
        amount_of_questions = len(self.electionquestion_set.all())

        # Get the maximum difference between the alternatives
        max_difference = abs(VALUES[0][0] - VALUES[-1][0])

        # Return maximum difference times amount of questions to get the maximum disagreement value
        return amount_of_questions * max_difference


class ElectionQuestion(models.Model):
    """
    ElectionQuestion model to store the question data.
    Fields:
        question_form: ForeignKey (related to ElectionQuestionForm)
        question: TextField (Text field containing the question text)
    Related:
        answer_set: queryset (Containing Answer models)
    """

    question_form = models.ForeignKey(
        ElectionQuestionForm, on_delete=models.CASCADE
    )
    question = models.TextField(max_length=300, verbose_name="Påstand")

    def __str__(self):
        """
        Returns the object name.
        returns:
            question: str (object question)
        """
        return self.question


class Answer(models.Model):
    """
    Answer model to store answer data.
    Fields:
        Answer: IntegerField (contains the question answer)
        question: ForeignKey (related to ElectionQuestion)
    """

    answer = models.IntegerField(choices=VALUES)
    question = models.ForeignKey(ElectionQuestion, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the object name.
        returns:
            name: str (question + answer)
        """
        return f"{self.question.question} Answer: {self.answer}"

    def get_name(self):
        """
        Returns the name of the user/committee who submitted the answer.
        'No name'  for basic Answer object without user/committee.
        returns:
            "No name"
        """
        return f"No name>"

    def get_election_form(self):
        """
        Returns the related ElectionQuestionForm object
        Returns:
            related ElectionQuestionForm
        """
        return self.question.question_form


class CommiteeAnswer(Answer):
    """
    CommiteeAnswer model to store answer data. Inherits from Answer.
    Fields:
        Answer: IntegerField (contains the question answer)
        question: ForeignKey (related to ElectionQuestion)
        committee: ForeignKey (related to Committee)
    """

    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

    def get_name(self):
        """
        Returns the name of the committee who submitted the answer.
        returns:
            committee_name: str
        """
        return self.committee.title


class UserAnswer(Answer):
    """
    UserAnswer model to store answer data. Inherits from Answer.
    Fields:
        Answer: IntegerField (contains the question answer)
        question: ForeignKey (related to ElectionQuestion)
        user: ForeignKey (related to User)
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_name(self):
        """
        Returns the name of the user who submitted the answer.
        returns:
            user_fullname: str
        """
        return f"{self.user.first_name} {self.user.last_name}"
