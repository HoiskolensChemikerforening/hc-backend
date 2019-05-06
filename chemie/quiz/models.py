from django.db import models
from django.contrib.auth.models import User


class QuizTerm(models.Model):
    """
    En QuizTerm er en quizperiode. Man samler opp poeng på hver quiz
    over en periode (f eks ett semester)

    term er navnet på quizperioden.
    is_active angir om quizperioden er den som gjelder nå.
    Om det opprettes en ny quizperiode som settes til aktiv (True), vil
    den nåværende aktive settes til inaktiv (False).
    """

    is_active = models.BooleanField(verbose_name='Aktiv Quiz')
    term = models.CharField(max_length=100, verbose_name='Quiz')

    def save(self, *args, **kwargs):
        if self.is_active:
            QuizTerm.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.term


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.ForeignKey(QuizTerm, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.score)
