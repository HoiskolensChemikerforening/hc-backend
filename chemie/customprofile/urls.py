from django.conf.urls import url

from . import views

app_name = "customprofile"

urlpatterns = [
    url(r"^profile/register$", views.register_user, name="register"),
    url(r"^profile/edit$", views.edit_profile, name="edit"),
    url(r"^profile/edit-push$", views.edit_push, name="edit-push"),
    url(
        r"^profile/forgotpassword",
        views.forgot_password,
        name="forgotpassword",
    ),
    url(
        r"^profile/aktiver/(?P<code>[a-z0-9]{32})/?",
        views.activate_password,
        name="activate",
    ),
    url(
        r"^profile/medlemmer/endre/(?P<profile_id>[0-9]+)",
        views.change_membership_status,
        name="membership",
    ),
    url(r"^profile/medlemmer", views.view_memberships, name="memberships"),
    url(r"^profile/add_card", views.add_rfid, name="add_rfid"),
    url(
        r"^yearbook/(?P<year>[0-9]+)/$", views.yearbook, name="yearbook-grade"
    ),
    url(r"^yearbook$", views.yearbook, name="yearbook-index"),
]
