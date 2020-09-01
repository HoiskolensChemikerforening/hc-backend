from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views

api_urlpatterns = [
    path("api/api-auth/", views.obtain_auth_token, name="obtain-auth-token"),
    path(
        "api/sladreboks/",
        include("chemie.shitbox.api.urls", namespace="shitbox-api"),
    ),
]
