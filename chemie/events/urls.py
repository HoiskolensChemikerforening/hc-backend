from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = "events"

# Events
urlpatterns = [
    path(
        "", login_required(views.ListSocialView.as_view()), name="index_social"
    ),
    path(
        "tidligere/",
        login_required(views.ListPastSocialView.as_view()),
        name="past_social",
    ),
    path(
        "administrer/",
        login_required(views.ListAdminSocialView.as_view()),
        name="admin_social",
    ),
    path("opprett/", views.CreateSocialView.as_view(), name="create_social"),
    path(
        "rediger/<int:pk>/", views.EditSocialView.as_view(), name="edit_social"
    ),
    path(
        "<int:pk>/",
        login_required(views.ViewSocialDetailsView.as_view()),
        name="detail_social",
    ),
    path(
        "registrer/<int:pk>/",
        login_required(views.SocialBaseRegisterUserView.as_view()),
        name="register_social",
    ),
    path(
        "adminliste/<int:pk>/",
        views.SocialEnlistedUsersView.as_view(),
        name="adminlist_social",
    ),
    path("<int:pk>/checkin/", views.check_in_to_social, name="checkin_social"),
    path(
        "adminliste/betalingsstatus/",
        views.change_payment_status,
        name="payment_status_social",
    ),
    path(
        "slett/<int:pk>/",
        views.DeleteSocialView.as_view(),
        name="delete_social",
    ),
    path(
        "adminliste/oppmotestatus/",
        views.change_arrival_status,
        name="arrival_status_social",
    ),
    path(
        "slett/",
        permission_required("events.delete_event")(
            views.ListSocialDeleteView.as_view()
        ),
        name="delete_list_social",
    ),
    path("api/social", views.SocialListCreate.as_view(), name="api_social"),
    path(
        "api/socialeventregistration",
        views.SocialEventRegistrationListCreate.as_view(),
        name="api_socialeventregistration",
    ),
    path("api/social/<int:pk>", views.SocialDetail.as_view()),
    path(
        "api/socialeventregistration/<int:pk>",
        views.SocialEventRegistrationDetail.as_view(),
    ),
]

# Bedpres
urlpatterns += [
    path("bedpres/", login_required(views.ListBedpresView.as_view()), name="index_bedpres"),
    path(
        "bedpres/tidligere/",
        views.ListPastBedpresView.as_view(),
        name="past_bedpres",
    ),
    path(
        "bedpres/opprett/",
        views.CreateBedpresView.as_view(),
        name="create_bedpres",
    ),
    path(
        "bedpres/rediger/<int:pk>/",
        views.EditBedpresView.as_view(),
        name="edit_bedpres",
    ),
    path(
        "bedpres/<int:pk>/",
        views.ViewBedpresDetailsView.as_view(),
        name="detail_bedpres",
    ),
    path(
        "bedpres/<int:pk>/sjekkinn/",
        views.checkin_to_bedpres,
        name="checkin_bedpres",
    ),
    path(
        "bedpres/registrer/<int:pk>/",
        views.BedpresBaseRegisterUserView.as_view(),
        name="register_bedpres",
    ),
    path(
        "bedpres/adminliste/<int:pk>/",
        views.BedpresEnlistedUsersView.as_view(),
        name="adminlist_bedpres",
    ),
    path(
        "bedpres/adminliste/oppmotestatus/",
        views.change_arrival_status,
        name="arrival_status_bedpres",
    ),
    path(
        "bedpres/slett/<int:pk>/",
        views.DeleteBedpresView.as_view(),
        name="delete_bedpres",
    ),
    path(
        "bedpres/slett/",
        views.ListBedpresDeleteView.as_view(),
        name="delete_list_bedpres",
    ),
    path("api/bedpres", views.BedpresListCreate.as_view(), name="api_bedpres"),
    path(
        "api/bedpresregistration",
        views.BedpresRegistrationListCreate.as_view(),
        name="api_bedpresregistration",
    ),
    path("api/bedpres/<int:pk>", views.BedpresDetail.as_view()),
    path(
        "api/bedpresregistration/<int:pk>",
        views.BedpresRegistrationDetail.as_view(),
    ),
]
