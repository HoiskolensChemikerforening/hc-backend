from django.urls import path
from .views import *
from .views import SubmissionListView, SubmissionDetailView

app_name = "shitbox"

urlpatterns = [
    path("api/", SubmissionListView.as_view()),
    path("api/<int:pk>/", SubmissionDetailView.as_view()),
    path("liste/", submissions_overview, name="list"),
    path("", post_votes, name="index"),
    path("toggle-used", toggle_used, name="toggle-used"),
]
