from . import views
from django.urls import path

app_name = "refound"

urlpatterns = [
    path("", views.index, name="index"),
    path("mine", views.my_refounds, name="myrefounds"),
    ]