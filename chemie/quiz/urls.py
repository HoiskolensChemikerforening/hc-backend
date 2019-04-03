from . import views
from django.conf.urls import url

app_name = "quiz"

urlpatterns = [
    url(
        r"^$",
        views.index,
        name="index",
    ),
    url(
        r"^create-term",
        views.create_term,
        name="create_term"
    ),
    url(
        r"^(?P<pk>[0-9]+)/delete-term",
        views.delete_term,
        name="delete_term"
    ),
    url(
        r"^(?P<pk>[0-9]+)/activate",
        views.activate_deactivate,
        name='activate_deactivate'
    ),
    url(
        r"^(?P<pk>[0-9]+)/$",
        views.term_detail,
        name="term_detail",
    ),
    url(
        r"^(?P<pk>[0-9]+)/create$",
        views.create_score,
        name="create_score",
    ),
    url(
        r"^(?P<pk>[0-9]+)/edit$",
        views.edit_score,
        name="edit_score"
    )
]
