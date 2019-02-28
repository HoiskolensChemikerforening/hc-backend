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
]
