from django.urls import path, re_path
from .views import *
from django.views.generic import TemplateView

app_name = "home"

urlpatterns = [
    path("", index, name="home"),
    path("kontakt/", contact, name="kontakt"),
    path("kalender/", calendar, name="calendar"),
    path("midler/", request_funds, name="fundsapplication"),
    path("kontortilgang/søk", request_office, name="officeaccess"),
    re_path(r"^flatpage/(?P<url>.*)$", edit_flatpage, name="edit_flatpage"),
    path(
        "kontortilgang/søkere",
        OfficeAccessApplicationListView.as_view(),
        name="office_access_list",
    ),
    path(
        "howToKontoret/",
        TemplateView.as_view(template_name="home/office_embedded_video.html"),
    ),
]
