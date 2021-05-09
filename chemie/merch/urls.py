from django.urls import path

from . import views

app_name="merch"

urlpatterns = [
    path("", views.all_merch, name="index"),
    path("opprett/", views.create_merch, name="create"),
]