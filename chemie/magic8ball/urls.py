from django.urls import path
from .views import eight_ball_view

app_name = "magic8ball"

urlpatterns = [
    path("", eight_ball_view, name="index"),
]
