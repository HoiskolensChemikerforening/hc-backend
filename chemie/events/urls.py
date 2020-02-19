from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

app_name = "events"

# Events
urlpatterns = [
    url(
        r"^social/$",
        login_required(views.ListSocialView.as_view()),
        name="index_social",
    ),
    url(
        r"^social/past",
        login_required(views.ListPastSocialView.as_view()),
        name="past_social",
    ),
    url(
        r"^social/create",
        views.CreateSocialView.as_view(),
        name="create_social",
    ),
    url(
        r"^social/edit/(?P<pk>[0-9]+)/$",
        views.EditSocialView.as_view(),
        name="edit_social",
    ),
    url(
        r"^social/(?P<pk>[0-9]+)/$",
        login_required(views.ViewSocialDetailsView.as_view()),
        name="detail_social",
    ),
    url(
        r"^social/register/(?P<pk>[0-9]+)",
        login_required(views.SocialBaseRegisterUserView.as_view()),
        name="register_social",
    ),
    path(
        "social/<int:pk>/checkin/",
        views.check_in_to_social,
        name="checkin_social",
         ),
    url(
        r"^social/adminlist/(?P<pk>[0-9]+)",
        views.SocialEnlistedUsersView.as_view(),
        name="adminlist_social",
    ),
    url(
        r"^social/adminlist/paymentstatus/(?P<registration_id>[0-9]+)",
        views.change_payment_status,
        name="payment_status_social",
    ),
    path(
        "social/adminlist/arrivalstatus/<int:registration_id>",
        views.change_arrival_status_social,
        name="arrival_status_social"
    ),
    url(
        r"^social/delete/(?P<pk>[0-9]+)",
        views.DeleteSocialView.as_view(),
        name="delete_social",
    ),
    url(
        r"^social/delete/",
        permission_required("events.delete_event")(
            views.ListSocialDeleteView.as_view()
        ),
        name="delete_list_social",
    ),
]

# Bedpres
urlpatterns += [
    url(r"^bedpres/$", views.ListBedpresView.as_view(), name="index_bedpres"),
    url(
        r"^bedpres/past",
        views.ListPastBedpresView.as_view(),
        name="past_bedpres",
    ),
    url(
        r"^bedpres/create",
        views.CreateBedpresView.as_view(),
        name="create_bedpres",
    ),
    url(
        r"^bedpres/edit/(?P<pk>[0-9]+)/$",
        views.EditBedpresView.as_view(),
        name="edit_bedpres",
    ),
    url(
        r"^bedpres/(?P<pk>[0-9]+)/$",
        views.ViewBedpresDetailsView.as_view(),
        name="detail_bedpres",
    ),
    url(
        r"^bedpres/(?P<pk>[0-9]+)/checkin/$",
        views.checkin_to_bedpres,
        name="checkin_bedpres",
    ),
    url(
        r"^bedpres/register/(?P<pk>[0-9]+)",
        views.BedpresBaseRegisterUserView.as_view(),
        name="register_bedpres",
    ),
    url(
        r"^bedpres/adminlist/(?P<pk>[0-9]+)",
        views.BedpresEnlistedUsersView.as_view(),
        name="adminlist_bedpres",
    ),
    url(
        r"^bedpres/adminlist/arrivalstatus/(?P<registration_id>[0-9]+)",
        views.change_arrival_status,
        name="arrival_status_bedpres",
    ),
    url(
        r"^bedpres/delete/(?P<pk>[0-9]+)",
        views.DeleteBedpresView.as_view(),
        name="delete_bedpres",
    ),
    url(
        r"^bedpres/delete",
        views.ListBedpresDeleteView.as_view(),
        name="delete_list_bedpres",
    ),
]
