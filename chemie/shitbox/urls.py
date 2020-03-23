from django.conf.urls import url
from django.urls import path
from .views import *

app_name = "shitbox"

urlpatterns = [
    url(r"list/$", submissions_overview, name="list"),
    url(r"list/(?P<page>[0-9]*)$", submissions_overview, name="list-page"),
    url(r"^$", post_votes, name="index"),
    path("toggle-used", toggle_used, name="toggle-used"),
]
