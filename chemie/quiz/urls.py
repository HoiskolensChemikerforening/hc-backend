from . import views
from django.conf.urls import url

app_name = "quiz"
#quiz
urlpatterns = [
    url(
        r"^$",
        views.index,
        name="index_quiz",

    ),
    url(
        r"^(?P<pk>[0-9]+)/$",
        views.quiz_term,
        name="quizterm",
    ),
]