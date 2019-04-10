from django.conf.urls import url
from chemie.committees.views import UserAutocomplete
from . import views
from . import views_admin

app_name = "elections"

admin_urlpatterns = [
    url(
        r"^admin/$",
        views_admin.admin_start_election,
        name="admin_start_election",
    ),
    url(
        r"^admin/end/$",
        views_admin.admin_end_election,
        name="admin_end_election",
    ),
    url(
        r"^admin/register/$",
        views_admin.admin_register_positions,
        name="admin_register_positions",
    ),
    url(
        r"^admin/register/delete/$",
        views_admin.admin_delete_position,
        name="admin_delete_position",
    ),
    url(
        r"^admin/register/(?P<pk>\d+)/$",
        views_admin.admin_register_candidates,
        name="admin_register_candidates",
    ),
    url(
        r"^admin/register/(?P<pk>\d+)/start$",
        views_admin.admin_start_voting,
        name="admin_start_voting",
    ),
    url(
        r"^admin/register/(?P<pk>\d+)/delete/$",
        views_admin.admin_delete_candidate,
        name="admin_delete_candidate",
    ),
    url(
        r"^admin/register/(?P<pk>\d+)/prevotes/$",
        views_admin.admin_register_prevotes,
        name="admin_register_prevotes",
    ),
    url(
        r"^admin/register/(?P<pk>\d+)/active",
        views_admin.admin_voting_is_active,
        name="admin_voting_active",
    ),
    url(
        r"^admin/results/(?P<pk>\d+)",
        views_admin.admin_results,
        name="admin_results",
    ),
    url(
        r"^user-autocomplete/",
        UserAutocomplete.as_view(),
        name="user-autocomplete",
    ),
]
user_urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^vote/$", views.vote, name="vote"),
    url(r"^vote/end", views.has_voted, name="has_voted"),
    url(r"^checkin/$", views_admin.change_rfid_status, name="checkin"),
]
urlpatterns = admin_urlpatterns + user_urlpatterns
