from django.urls import path

from . import views

app_name = "committees"

urlpatterns = [
    path("", views.index, name="list_all"),
    path(
        "user-autocomplete/",
        views.UserAutocomplete.as_view(),
        name="user-autocomplete",
    ),
    path("<slug:slug>/", views.view_committee, name="committee_detail"),
    path(
        "<slug:slug>/rediger/", views.edit_description, name="edit_description"
    ),
    path(
        "<slug:slug>/rediger-medlemmmer/",
        views.edit_committee_memberships,
        name="edit_memberships",
    ),
]
