from . import views
from django.urls import path


app_name = "MatMaster"


urlpatterns = [path("", views.index, name="index"),
               path("form/", views.createRecipes, name = "form")]