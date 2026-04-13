from django.urls import path
from .views import spin_wheel_view

app_name = "spinwheel"

urlpatterns = [
    path("", spin_wheel_view, name="index"),
]