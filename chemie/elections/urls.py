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
        r"^admin/avslutt/$",
        views_admin.admin_end_election,
        name="admin_end_election",
    ),
    url(
        r"^admin/registrer/$",
        views_admin.admin_register_positions,
        name="admin_register_positions",
    ),
    url(
        r"^admin/registrer/slett/$",
        views_admin.admin_delete_position,
        name="admin_delete_position",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/$",
        views_admin.admin_register_candidates,
        name="admin_register_candidates",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/start$",
        views_admin.admin_start_voting,
        name="admin_start_voting",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/slett/$",
        views_admin.admin_delete_candidate,
        name="admin_delete_candidate",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/forhaandsstemmer/$",
        views_admin.admin_register_prevotes,
        name="admin_register_prevotes",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/akklamasjon/$",
        views_admin.admin_acclamation,
        name="admin_acclamation",
    ),
    url(
        r"^admin/registrer/(?P<pk>\d+)/aktiv",
        views_admin.admin_voting_is_active,
        name="admin_voting_active",
    ),
    url(
        r"^admin/resultater/(?P<pk>\d+)",
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
    url(r"^stem/$", views.vote, name="vote"),
    url(r"^stem/ferdig", views.has_voted, name="has_voted"),
    url(r"^sjekkinn/$", views_admin.change_rfid_status, name="checkin"),
    url(r"^manuell-sjekkinn/$", views_admin.manual_rfid_status, name="checkin-manually"),
    url(r"^tidligere-valg/$", views.view_previous_elections_index, name="previous_index"),
    url(r"^tidligere-valg/(?P<pk>\d+)", views.view_previous_election, name="previous_election"),
]
urlpatterns = admin_urlpatterns + user_urlpatterns
