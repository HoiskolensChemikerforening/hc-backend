from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import submissions_overview, post_votes
from .views import CreateView, DetailsView
from rest_framework.authtoken import views as rest_framework_views

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'list/$', submissions_overview, name='list'),
    url(r'list/(?P<page>[0-9]*)$', submissions_overview, name='list-page'),
    url(r'^$', post_votes, name="index"),
    url(r'^rest/$', CreateView.as_view(), name='create'),
    url(r'^rest/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
"""urllene for REST API må flyttes til API/Sladderboks"""
