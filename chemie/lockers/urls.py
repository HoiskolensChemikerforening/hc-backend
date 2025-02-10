from django.urls import path, re_path

from . import views

app_name = "lockers"

urlpatterns = [
    path("", views.view_lockers, name="index"),
    path("registrer/<int:number>/", views.register_locker, name="registrer"),
    re_path(
        r"^aktiver/(?P<code>[a-z0-9]{32})/?",
        views.activate_ownership,
        name="activate",
    ),
    path(
        "administrer/slett/<int:locker_number>/",
        views.clear_locker,
        name="force-remove",
    ),
    path("administrer/", views.manage_lockers, name="administrate"),
    re_path(
        r"^administrer/#(?P<anchor>[-_\w]+)$",
        views.manage_lockers,
        name="administrate",
    ),
    path("mine-skap/", views.my_lockers, name="mineskap"),
    path("api/locker/", views.LockerListCreate.as_view(), name="api_lockers"),
    path(
        "api/lockeruser/",
        views.LockerUserListCreate.as_view(),
        name="api_lockeruser",
    ),
    path(
        "api/ownership/",
        views.OwnershipListCreate.as_view(),
        name="api_ownership",
    ),
    path(
        "api/lockertoken/",
        views.LockerTokenListCreate.as_view(),
        name="api_lockertoken",
    ),
    path("api/locker/<int:pk>", views.LockerDetail.as_view()),
    path("api/lockeruser/<int:pk>", views.LockerUserDetail.as_view()),
    path("api/ownership/<int:pk>", views.OwnershipDetail.as_view()),
    path("api/lockertoken/<int_pk>", views.LockerTokenDetail.as_view()),
    path("Bokskapregler/", views.renderRules, name="renderRules"),
]
