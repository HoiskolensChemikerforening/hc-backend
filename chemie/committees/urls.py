from django.conf.urls import include, url

from . import views

app_name = "committees"

urlpatterns = [
    url(r"^$", views.index, name="list_all"),
    url(
        r"^user-autocomplete/",
        views.UserAutocomplete.as_view(),
        name="user-autocomplete",
    ),
    url(r"^(?P<slug>[\w-]+)/$", views.view_committee, name="committee_detail"),
    url(
        r"^(?P<slug>[\w-]+)/edit/",
        views.edit_description,
        name="edit_description",
    ),
    url(
        r"^(?P<slug>[\w-]+)/edit-members/",
        views.edit_committee_memberships,
        name="edit_memberships",
    ),
]
