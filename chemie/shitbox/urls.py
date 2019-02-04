from django.conf.urls import url
from .views import submissions_overview, post_votes

app_name = "shitbox"

urlpatterns = [
    url(r"list/$", submissions_overview, name="list"),
    url(r"list/(?P<page>[0-9]*)$", submissions_overview, name="list-page"),
    url(r"^$", post_votes, name="index"),
]
