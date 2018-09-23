from django.conf.urls import url
from chemie.committees.views import UserAutocomplete
from . import views

admin_urlpatterns = [
    url(r'^admin/$', views.admin_start_election, name='admin_start_election'),
    url(r'^admin/end/$', views.admin_end_election, name='admin_end_election'),
    url(r'^admin/register/$', views.admin_register_positions, name='admin_register_positions'),
    url(r'^admin/register/(?P<pk>\d+)/$', views.admin_register_candidates, name='admin_register_candidates'),
    url(r'^admin/register/(?P<pk>\d+)/start', views.admin_voting_is_active, name='admin_start_voting'),
    url(r'^admin/register/(?P<pk>\d+)/results', views.admin_results, name='admin_results'),
    url(r'^user-autocomplete/', UserAutocomplete.as_view(), name='user-autocomplete',),
]
user_urlpatterns = [
    url(r'^$', views.vote, name='vote'),
    url(r'^vote/$', views.voting, name='voting'),
    url(r'^vote/end', views.has_voted, name='has_voted'),
    url(r'^results', views.resultater, name='resultater')
]
urlpatterns = admin_urlpatterns + user_urlpatterns
