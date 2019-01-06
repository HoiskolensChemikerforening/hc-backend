from django.conf.urls import url

from . import views

app_name = "yearbook"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^(?P<year>[0-9]+)/$", views.index),
]
