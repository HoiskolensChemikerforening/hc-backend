from django.urls import path

from . import views

app_name = "yearbook"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/", views.index),
]
