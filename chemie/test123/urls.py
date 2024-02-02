from django.urls import path

from .views import testViews

app_name = "test"

urlpatterns = [path("", testViews, name="test123")]