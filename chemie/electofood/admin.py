from django.contrib import admin
from .models import (
    ElectionQuestionForm,
    ElectionQuestion,
    CommiteeAnswer,
    UserAnswer,
)

admin.site.register(ElectionQuestionForm)
admin.site.register(ElectionQuestion)
admin.site.register(CommiteeAnswer)
admin.site.register(UserAnswer)
