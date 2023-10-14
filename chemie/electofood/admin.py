from django.contrib import admin
from .models import (
    ElectionQuestionForm,
    ElectionQuestion,
    CommiteeAnswer,
    UserAnswer,
)

admin.site.register(ElectionQuestionForm)


@admin.register(ElectionQuestion)
class ElectionQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "question_form"]


@admin.register(CommiteeAnswer)
class CommiteeAnswerAdmin(admin.ModelAdmin):
    list_display = ["committee", "question", "answer", "get_election_form"]


# admin.site.register(CommiteeAnswer)
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "answer", "get_election_form"]
