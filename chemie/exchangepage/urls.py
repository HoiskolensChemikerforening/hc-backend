from . import views
from django.urls import path

app_name = "exchangepage"

urlpatterns = [path("", views.index, name="index")]