from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = "events"

# Sosial
urlpatterns = [
    path("", login_required(views.ListSocialView.as_view()), name="index_social"),
    path("tidligere/",login_required(views.ListPastSocialView.as_view()),name="past_social"),
    path("administrer/",login_required(views.ListAdminSocialView.as_view()),name="admin_social"),
    path("opprett/", views.CreateSocialView.as_view(), name="create_social"),
    path("rediger/<int:pk>/", views.EditSocialView.as_view(), name="edit_social"),
    path("<int:pk>/", login_required(views.ViewSocialDetailsView.as_view()), name="detail_social"),
    path("registrer/<int:pk>/", login_required(views.SocialBaseRegisterUserView.as_view()), name="register_social"),
    path("adminliste/<int:pk>/", views.SocialEnlistedUsersView.as_view(), name="adminlist_social"),
    path("<int:pk>/checkin/", views.check_in_to_social, name="checkin_social"),
    path("adminliste/betalingsstatus/", views.change_payment_status, name="payment_status_social"),
    path("slett/<int:pk>/", views.DeleteSocialView.as_view(), name="delete_social"),
    path("adminliste/oppmotestatus/", views.change_arrival_status, name="arrival_status_social"),
    path("slett/", permission_required("events.delete_event")(views.ListSocialDeleteView.as_view()), name="delete_list_social"),

    #API
    path("api/sosial/", views.SocialListCreate.as_view(), name="api_sosial"),
    path("api/sosial/kommende/", views.SocialListCreateKommende.as_view(), name="api_sosial_kommende"),
    path("api/sosialregistrering/", views.SocialEventRegistrationListCreate.as_view(), name="api_sosialregistrering"),
    path("api/sosial/<int:pk>/", views.SocialDetail.as_view()),
    path("api/sosialregistrering/<int:pk>/",views.SocialEventRegistrationDetail.as_view()),
    path("api/sosial/mine/", views.SocialListCreateMine.as_view(), name="api_sosial_mine"),
    path("api/sosial/tidligere/", views.SocialListCreateTidligere.as_view(), name="api_sosial_tidligere"),
    path("api/sosial/opprett/", views.SocialDetailCreate.as_view(), name="api_detail_opprett"),
    path("api/sosial/slett/<int:pk>", views.SocialDetailDelete.as_view(), name="api_detail_slett"),
    path("api/sosial/rediger/<int:pk>", views.SocialDetailUpdate.as_view(), name="api_detail_rediger"),
    path("api/sosial/slett/", views.SocialDelete.as_view(), name="api_slett"),
    path("api/sosial/administrer/", views.SocialAdministrate.as_view(), name="api_sosial_administrer")
]

# Karriere
urlpatterns += [
    path("bedpres/", views.ListBedpresView.as_view(), name="index_bedpres"),
    path("bedpres/tidligere/",views.ListPastBedpresView.as_view(),name="past_bedpres"),
    path("bedpres/opprett/", views.CreateBedpresView.as_view(),name="create_bedpres"),
    path("bedpres/rediger/<int:pk>/", views.EditBedpresView.as_view(),name="edit_bedpres"),
    path("bedpres/<int:pk>/", views.ViewBedpresDetailsView.as_view(),name="detail_bedpres"),
    path("bedpres/<int:pk>/sjekkinn/", views.checkin_to_bedpres,name="checkin_bedpres"),
    path("bedpres/registrer/<int:pk>/", views.BedpresBaseRegisterUserView.as_view(),name="register_bedpres"),
    path("bedpres/adminliste/<int:pk>/", views.BedpresEnlistedUsersView.as_view(), name="adminlist_bedpres"),
    path("bedpres/adminliste/oppmotestatus/", views.change_arrival_status, name="arrival_status_bedpres"),
    path("bedpres/slett/<int:pk>/", views.DeleteBedpresView.as_view(), name="delete_bedpres"),
    path("bedpres/slett/", views.ListBedpresDeleteView.as_view(), name="delete_list_bedpres"),

    #API
    path("api/karriere/", views.BedpresListCreate.as_view(), name="api_karriere"),
    path("api/karriereregistrering/", views.BedpresRegistrationListCreate.as_view(), name="api_karriereregistrering"),
    path("api/karriere/<int:pk>/", views.BedpresDetail.as_view()),
    path("api/karriereregistrering/<int:pk>/", views.BedpresRegistrationDetail.as_view()),
    path("api/karriere/kommende/", views.BedpresListKommende.as_view(), name="api_karriere_kommende"),
    path("api/karriere/tidligere/", views.BedpresListTidligere.as_view(), name="api_karriere_tidligere"),
    path("api/karriere/mine/", views.BedpresListCreateMine.as_view(), name="api_karriere_mine"),
    path("api/karriere/opprett/", views.BedpresDetailCreate.as_view(), name="api_karriere_opprett"),
    path("api/karriere/rediger/<int:pk>/", views.BedpresUpdate.as_view(), name="api_karriere_rediger"),
    path("api/karriere/slett/", views.BedpresDelete.as_view(), name="api_slett")
]
