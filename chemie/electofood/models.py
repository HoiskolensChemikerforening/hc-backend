from django.db import models
from chemie.committees.models import Committee
from django.contrib.auth.models import User

VALUES = (
        (-3, "Helt uenig"),
        (-2, "Litt uenig"),
        (2,  "Litt enig"),
        (3,  "Helt enig"),
    )

class ElectionQuestionForm(models.Model):
    title = models.CharField(max_length=40, verbose_name="Tittel")
    description = models.TextField(max_length=300, default="", verbose_name="Beskrivelse")
    active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return self.title

    def calculate_result_commitee(self, user, committee):
        disagreement_sum = 0
        for question in self.electionquestion_set.all():
            answer = question.answer_set.filter(useranswer__user=user)
            commitee_answer = question.answer_set.filter(commiteeanswer__committee=committee)
            disagreement_sum += abs(answer[0].answer - commitee_answer[0].answer)
        max_disagreement_sum = self.get_max_disagreement_sum()
        return int((1 - (disagreement_sum/max_disagreement_sum))*100)

    def get_participating_committes(self):
        committes = []
        for committe in Committee.objects.all():
            if not 0 in [len(q.answer_set.filter(commiteeanswer__committee=committe)) for q in self.electionquestion_set.all()]:
                committes.append(committe)
        return committes

    def get_max_disagreement_sum(self):
        amount_of_questions = len(self.electionquestion_set.all())
        max_difference = abs(VALUES[0][0] - VALUES[-1][0])
        return amount_of_questions*max_difference



class ElectionQuestion(models.Model):
    question_form = models.ForeignKey(ElectionQuestionForm, on_delete=models.CASCADE)
    question = models.TextField(max_length=300, verbose_name="Påstand")

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.IntegerField(
        choices=VALUES
    )
    question = models.ForeignKey(ElectionQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.question} Answer: {self.answer}"

    def get_name(self):
        return f"No name>"

    def get_election_form(self):
        return self.question.question_form


class CommiteeAnswer(Answer):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    def get_name(self):
        return self.committee.title

class UserAnswer(Answer):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

