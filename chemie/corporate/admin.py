from django.contrib import admin
from .models import (
    Specialization,
    Interview,
    Job,
    Survey,
    SurveyQuestion,
    AnswerKeyValuePair,
    PositionType
)

admin.site.register(Interview)
admin.site.register(Specialization)
admin.site.register(Job)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(AnswerKeyValuePair)
admin.site.register(PositionType)
