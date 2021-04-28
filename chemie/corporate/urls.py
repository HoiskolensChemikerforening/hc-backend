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
    path(
        "intervju/<int:id>/rediger/",
        views.interview_edit,
        name="interview_edit",
    ),
    path("jobb/", views.job, name="job"),
    path("jobb/ny/", views.job_create, name="job_create"),
    path(
        "jobb/<int:id>/", views.job_detail, name="job_detail"
    ),
    path("jobb/<int:id>/fjern/", views.job_delete, name="job_delete"),
    path(
        "jobb/<int:id>/rediger/",
        views.job_edit,
        name="job_edit",
    ),
    path("diplom/", views.statistics, name="statistics"),
]
