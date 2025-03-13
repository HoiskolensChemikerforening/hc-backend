from . import views
from django.urls import path

app_name = "villsvin"

urlpatterns = [path("", views.index, name="index"), 
               path("form/", views.createVillsvin, name = "form") ]

