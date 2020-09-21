from django.urls import path
from . import views

app_name = "corporate"


urlpatterns = [
    path("", views.index, name="index"),
    path("intervju/", views.interview_list, name="interview_list"),
    path("intervju/lag", views.interview_create, name="interview_create"),
    path("intervju/<int:interview_id>/", views.interview_detail, name="interview_detail"),
]
