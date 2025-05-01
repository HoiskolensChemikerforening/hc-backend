from . import views
from django.urls import path


app_name = "matlab"


urlpatterns = [path("", views.index, name="index"),
               path("lageoppskrift/", views.createRecipes, name = "lageoppskrift"),
               path("oppskriftbeskrivelse/<int:pk>", views.detail, name = "oppskriftbeskrivelse")]