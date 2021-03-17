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
        views.interview_remove,
        name="interview_delete",
    ),
    path("jobb/", views.job_advertisement, name="job_advertisement"),
    path("jobb/ny/", views.job_create, name="job_create"),
    path("jobb/<int:id>/fjern/", views.job_remove, name="job_delete"),
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
        "diplom/undersøkelse/<int:year>/slett/",
        views.survey_delete,
        name="survey_delete",
    ),
    path("diplom/<int:year>/svar/ny/<str:question>/", views.answer_create, name="answer_create"),
    path("diplom/svar/rediger/", views.answer_edit, name="answer_edit"),
    path(
        "diplom/svar/<int:id>/slett/",
        views.answer_delete,
        name="answer_delete",
    ),
]
