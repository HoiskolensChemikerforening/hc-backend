from django.conf.urls import url
from django.urls import path

from . import views

app_name = "picturecarousel"

urlpatterns = [
    url(r"^send/", views.submit_picture, name="submit"),
    url(r"^$", views.view_carousel, name="display"),
    path("overview/", views.approve_pictures, name="overview"),
    path(
        "overview/<int:page>", views.approve_pictures, name="overview_detail"
    ),
    url(
        r"^overview/approve/(?P<picture_id>[0-9]+)",
        views.approve_deny,
        name="approve",
    ),
    url(
        r"^overview/deny/(?P<picture_id>[0-9]+)",
        views.approve_deny,
        {"deny": True},
        name="deny",
    ),
    path("bilder/", views.view_pictures, name="view_pictures"),
    path(
        "bilder/<int:page>", views.view_pictures, name="view_pictures_detail"
    ),
]
