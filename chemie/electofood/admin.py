from django.contrib import admin
from .models import (
    ElectionQuestionForm,
    ElectionQuestion,
    CommiteeAnswer,
    UserAnswer,
)

# Registrer ElectionQuestionForm
admin.site.register(ElectionQuestionForm)

# Registrer ElectionQuestion
@admin.register(ElectionQuestion)
class ElectionQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "question_form"]

# Registrer CommiteeAnswer
@admin.register(CommiteeAnswer)
class CommiteeAnswerAdmin(admin.ModelAdmin):
    list_display = ["committee", "question", "answer", "get_election_form"]


# Registrer UserAnswer
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "answer", "get_election_form"]
