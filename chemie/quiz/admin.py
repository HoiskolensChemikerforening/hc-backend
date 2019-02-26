from django.contrib import admin
from .models import QuizScore, QuizTerm
# Register your models here.

admin.site.register(QuizTerm)
admin.site.register(QuizScore)
