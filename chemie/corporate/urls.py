from django.urls import path
from . import views

app_name = "corporate"


urlpatterns = [
    path("", views.index, name="index"),
    path("intervju/ny", views.interview_create, name="interview_create"),
    path("intervju/<int:id>/fjern/", views.interview_remove, name="interview_delete"),
    path("jobb/ny", views.job_create, name="job_create"),
    path("jobb/<int:id>/fjern/", views.job_remove, name="job_delete"),
]
