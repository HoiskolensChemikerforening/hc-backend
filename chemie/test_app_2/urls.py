from django.urls import path
from . import views

app_name = "test_app_2"

urlpatterns = [
    path("", views.index, name="index"),
    path("krokodille_2/", views.index_2, name="index_2"),
    path("../test_app/", views.dih, name="noe")
]