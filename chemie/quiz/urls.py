from . import views
from django.urls import path

app_name = "quiz"

urlpatterns = [
    path("", views.index, name="index"),
    path("poeng/api/", views.ListAllScores.as_view()),
    path("periode/api/", views.ListAllQuizTerms.as_view()),
    path("poeng-detaljer/api/<int:pk>", views.QuizTermDetail.as_view()),
    path("periode-detaljer/api/<int:pk>", views.QuizScoreDetail.as_view()),
    path("navnequiz", views.name_quiz_index, name="name_quiz_index"),
    path("navnequiz/<int:year>", views.name_quiz, name="name_quiz"),
    path("arrkomquiz", views.arrkom_index, name="arrkomquiz_index"),
    path("ny", views.create_term, name="create_term"),
    path("<int:pk>/slett", views.delete_term, name="delete_term"),
    path(
        "<int:pk>/aktiver",
        views.activate_deactivate,
        name="activate_deactivate",
    ),
    path("<int:pk>/", views.term_detail, name="term_detail"),
    path("<int:pk>/rediger", views.create_score, name="create_score"),
    path("<int:pk>/endre-poeng", views.edit_scores, name="edit_scores"),
]
