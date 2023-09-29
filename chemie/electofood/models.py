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

    def __str__(self):
        return self.title

    def calculate_result_commitee(self, user, committee):
        disagreement_sum = 0
        print(1)
        for question in self.electionquestion_set.all():
            answer = question.useranswer_set.filter(user=user)
            commitee_answer = question.commiteeanswer_set.filter(committee=committee)
            disagreement_sum += abs(answer[0].answer - commitee_answer)
        return disagreement_sum



class ElectionQuestion(models.Model):
    question_form = models.ForeignKey(ElectionQuestionForm, on_delete=models.CASCADE)
    question = models.TextField(max_length=40, verbose_name="Påstand")

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.IntegerField(
        choices=VALUES
    )
    question = models.ForeignKey(ElectionQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.question} Answer: {self.answer}"

class CommiteeAnswer(Answer):
    committee = models.ForeignKey(Committee,on_delete=models.CASCADE)

class UserAnswer(Answer):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

