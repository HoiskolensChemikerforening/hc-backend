from . import views
from django.urls import path


app_name = "matlab"


urlpatterns = [path("", views.index, name="index"),
               path("form/", views.createRecipes, name = "form")]