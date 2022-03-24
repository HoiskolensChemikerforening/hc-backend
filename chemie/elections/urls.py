from django.urls import path
from chemie.committees.views import UserAutocomplete
from . import views
from . import views_admin

app_name = "elections"

admin_urlpatterns = [
    path(
        "admin/", views_admin.admin_start_election, name="admin_start_election"
    ),
    path(
        "admin/avslutt/",
        views_admin.admin_end_election,
        name="admin_end_election",
    ),
    path(
        "admin/registrer/",
        views_admin.admin_register_positions,
        name="admin_register_positions",
    ),
    path(
        "admin/registrer/slett/",
        views_admin.admin_delete_position,
        name="admin_delete_position",
    ),
    path(
        "admin/registrer/<int:pk>/",
        views_admin.admin_register_candidates,
        name="admin_register_candidates",
    ),
    path(
        "admin/registrer/<int:pk>/start/",
        views_admin.admin_start_voting,
        name="admin_start_voting",
    ),
    path(
        "admin/registrer/<int:pk>/slett/",
        views_admin.admin_delete_candidate,
        name="admin_delete_candidate",
    ),
    path(
        "admin/registrer/<int:pk>/forhaandsstemmer/",
        views_admin.admin_register_prevotes,
        name="admin_register_prevotes",
    ),
    path(
        "admin/registrer/<int:pk>/akklamasjon/",
        views_admin.admin_acclamation,
        name="admin_acclamation",
    ),
    path(
        "admin/registrer/<int:pk>/aktiv/",
        views_admin.admin_voting_is_active,
        name="admin_voting_active",
    ),
    path(
        "admin/resultater/<int:pk>/",
        views_admin.admin_results,
        name="admin_results",
    ),
    path(
        "user-autocomplete/",
        UserAutocomplete.as_view(),
        name="user_autocomplete",
    ),
]
user_urlpatterns = [
    path("", views.index, name="index"),
    path("stem/", views.vote, name="vote"),
    path("stem/ferdig", views.has_voted, name="has_voted"),
    path("sjekkinn/", views_admin.change_rfid_status, name="checkin"),
    path(
        "manuell-sjekkinn/",
        views_admin.manual_rfid_status,
        name="checkin_manually",
    ),
]

api_urlpatterns = [
    path("cgp/api/", views.CandidateListView.as_view()),
]

urlpatterns = admin_urlpatterns + user_urlpatterns + api_urlpatterns


"""
    path(
        "tidligere-valg/",
        views.view_previous_elections_index,
        name="previous_index",
    ),
    path(
        "tidligere-valg/<int:pk>/)",
        views.view_previous_election,
        name="previous_election",
    )
"""

# The links for previous elections are commented out, because we don't want people to have access to them
