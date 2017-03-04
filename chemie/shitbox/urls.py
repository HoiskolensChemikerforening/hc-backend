from django.conf.urls import url

from .views import submissions_overview, post_votes

urlpatterns = [
    url(r'list/(?P<page>[0-9]+)$', submissions_overview, name='list'),
    url(r'^$', post_votes, name="index"),
]
