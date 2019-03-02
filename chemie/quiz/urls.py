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
