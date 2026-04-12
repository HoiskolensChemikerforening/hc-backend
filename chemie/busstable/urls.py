from django.urls import path

from django.urls import path
from . import views

app_name = "busstable"

urlpatterns = [
    path("", views.index, name="index"),
]