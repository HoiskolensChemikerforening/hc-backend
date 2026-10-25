from django.urls import path
from chemie.committees.views import UserAutocomplete
from chemie.preferansevalg import views
from chemie.preferansevalg import views_admin

app_name = "preferansevalg"

admin_urlpatterns = [
    path(
        "admin/", views_admin.admin_start_election, name="admin_start_election_pref"
    ),
    path(
        "admin/avslutt/",
        views_admin.admin_end_election,
        name="admin_end_election_pref",
    ),
    path(
        "admin/registrer/",
        views_admin.admin_register_positions,
        name="admin_register_positions_pref",
    ),
    path(
        "admin/registrer/slett/",
        views_admin.admin_delete_position,
        name="admin_delete_position_pref",
    ),
    path(
        "admin/registrer/<int:pk>/",
        views_admin.admin_register_candidates,
        name="admin_register_candidates_pref",
    ),
    path(
        "admin/registrer/<int:pk>/start/",
        views_admin.admin_start_voting,
        name="admin_start_voting_pref",
    ),
    path(
        "admin/registrer/<int:pk>/slett/",
        views_admin.admin_delete_candidate,
        name="admin_delete_candidate_pref",
    ),
    path(
        "admin/registrer/<int:pk>/forhaandsstemmer/",
        views_admin.admin_register_prevotes,
        name="admin_register_prevotes_pref",
    ),
    path(
        "admin/registrer/<int:pk>/akklamasjon/",
        views_admin.admin_acclamation,
        name="admin_acclamation_pref",
    ),
    path(
        "admin/registrer/<int:pk>/aktiv/",
        views_admin.admin_voting_is_active,
        name="admin_voting_active_pref",
    ),
    path(
        "admin/resultater/<int:pk>/",
        views_admin.admin_results,
        name="admin_results_pref",
    ),
    path(
        "user-autocomplete/",
        UserAutocomplete.as_view(),
        name="user_autocomplete",
    ),
    path(
        "open-election-for-everyone/",
        views_admin.open_election_for_everyone,
        name="open_election_for_everyone_pref",
    ),
]
user_urlpatterns = [
    path("", views.index, name="index"),
    path("stem/", views.vote, name="vote_pref"),
    path("stem/ferdig", views.has_voted, name="has_voted_pref"),
    path("sjekkinn/", views_admin.change_rfid_status, name="checkin_pref"),
    path(
        "manuell-sjekkinn/",
        views_admin.manual_rfid_status,
        name="checkin_manually_pref",
    ),
]
urlpatterns = admin_urlpatterns + user_urlpatterns
