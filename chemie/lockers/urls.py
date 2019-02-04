from django.conf.urls import url

from . import views

app_name = "lockers"

urlpatterns = [
    url(r"^$", views.view_lockers, name="index"),
    url(r"^(?P<page>[0-9]+)$", views.view_lockers, name="detail"),
    url(
        r"^registrer/(?P<number>[0-9]+)/$",
        views.register_locker,
        name="registrer",
    ),
    url(
        r"^aktiver/(?P<code>[a-z0-9]{32})/?",
        views.activate_ownership,
        name="activate",
    ),
    url(
        r"^administrer/slett/(?P<locker_number>[0-9]+)/",
        views.clear_locker,
        name="force-remove",
    ),
    url(r"^administrer", views.manage_lockers, name="administrate"),
    url(
        r"^administrer/#(?P<anchor>[-_\w]+)$",
        views.manage_lockers,
        name="administrate",
    ),
    url(r"^mine-skap", views.my_lockers, name="mineskap"),
]
