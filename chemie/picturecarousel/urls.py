from django.conf.urls import url
from django.urls import path
from .views import PictureTagAutocomplete
from . import views

app_name = "picturecarousel"

urlpatterns = [
    url(r"^send/",
        views.submit_picture,
        name="submit"),
    url(r"^$",
        views.view_carousel,
        name="display"),
    url(r"^overview/$",
        views.approve_pictures,
        name="overview"),
    url(r"^overview/(?P<page>[0-9]+)$",
        views.approve_pictures,
        name="detail"),
    url(r"^active/$",
        views.active_list,
        name="active"),
    url(r"^active/(?P<page>[0-9]+)$",
        views.active_list,
        name="active_detail"),
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
    url(
        r"^picturetag-autocomplete/",
        PictureTagAutocomplete.as_view(create_field='tag'),
        name='picturetag-autocomplete'
    ),
    path(
        'bilder/',
        views.view_pictures,
        name='view_pictures'
    ),
    path(
        'bilder/<int:page>',
        views.view_pictures,
        name="view_detail"),
]
