from django.urls import path
from . import views

app_name = "corporate"

urlpatterns = [
    path("", views.index, name="index"),
    path("intervju/", views.interview, name="interview"),
    path("intervju/ny/", views.interview_create, name="interview_create"),
    path(
        "intervju/<int:id>/", views.interview_detail, name="interview_detail"
    ),
    path(
        "intervju/<int:id>/fjern/",
        views.interview_delete,
        name="interview_delete",
    ),
    path("arrangementer/", views.events, name="events"),
    path(
        "intervju/<int:id>/rediger/",
        views.interview_edit,
        name="interview_edit",
    ),
    path("jobb/", views.job, name="job"),
    path("jobb/ny/", views.job_create, name="job_create"),
    path("jobb/<int:id>/", views.job_detail, name="job_detail"),
    path("jobb/<int:id>/fjern/", views.job_delete, name="job_delete"),
    path("jobb/<int:id>/rediger/", views.job_edit, name="job_edit"),
    path("diplom/", views.survey, name="statistics"),
    path("diplom/<int:year>/", views.survey, name="survey_year"),
    path("diplom/<int:id>/data/", views.ChartData.as_view()),
    path("diplom/admin/", views.statistics_admin, name="statistics_admin"),
    path(
        "diplom/undersøkelse/<int:year>/rediger/",
        views.survey_edit,
        name="survey_edit",
    ),
    path(
        "diplom/undersøkelse/fjern-spørsmål/",
        views.survey_remove_question,
        name="survey_remove_question",
    ),
    path(
        "diplom/undersøkelse/<int:year>/slett/",
        views.survey_delete,
        name="survey_delete",
    ),
    path(
        "diplom/nytt-spørsmål/", views.question_create, name="question_create"
    ),
    path(
        "diplom/rediger-spørsmål/", views.question_edit, name="question_edit"
    ),
    path(
        "diplom/slett-spørsmål/<int:id>/",
        views.question_delete,
        name="question_delete",
    ),
    path(
        "diplom/<int:year>/legg-til-spørsmål/",
        views.add_question_to_survey,
        name="question_add_to_survey",
    ),
    path(
        "diplom/<int:year>/svar/ny/<str:question>/",
        views.answer_create,
        name="answer_create",
    ),
    path("diplom/svar/rediger/", views.answer_edit, name="answer_edit"),
    path(
        "diplom/svar/<int:id>/slett/",
        views.answer_delete,
        name="answer_delete",
    ),
]
