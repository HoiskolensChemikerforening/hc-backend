from django.urls import path
from .views import *

app_name = "shitbox"

urlpatterns = [
    path("liste/", submissions_overview, name="list"),
    path("", post_votes, name="index"),
    path("toggle-used", toggle_used, name="toggle-used"),
]
