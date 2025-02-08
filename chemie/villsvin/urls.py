from . import views
from django.urls import path

app_name = "villsvin"

urlpatterns = [path("", views.index, name="index"), ]

