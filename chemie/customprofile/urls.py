from django.urls import path, re_path

from . import views

app_name = "customprofile"

urlpatterns = [
    path("profil/registrer/", views.register_user, name="register"),
    path("profil/rediger/", views.edit_profile, name="edit"),
    path("profil/rediger-push-varsler/", views.edit_push, name="edit-push"),
    path(
        "profil/glemt-passord/", views.forgot_password, name="forgotpassword"
    ),
    re_path(
        r"^profil/aktiver/(?P<code>[a-z0-9]{32})/?",
        views.activate_password,
        name="activate",
    ),
    path(
        "profil/medlemmer/endre/<int:profile_id>/<int:duration>/",
        views.change_membership_status,
        name="membership",
    ),
    path("profil/medlemmer/", views.view_memberships, name="memberships"),
    path(
        "profil/medlemmer/<int:year>",
        views.view_memberships,
        name="memberships-grade",
    ),
    path("profil/studentkort/", views.add_rfid, name="add_rfid"),
    path("katalog/<int:year>/", views.yearbook, name="yearbook-grade"),
    path("katalog/<int:year>/<int:spec>/", views.yearbook, name="yearbook-spec"),
    path("katalog/", views.yearbook, name="yearbook-index"),

    #API
    path("api/profil/", views.ProfileListCreate.as_view(), name="api-profile-list",),
    path("api/profil/<int:pk>/", views.ProfileDetail.as_view(), name="api-profile-detail",),
]
