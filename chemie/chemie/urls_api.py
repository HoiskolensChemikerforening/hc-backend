from django.conf.urls import url
from django.conf.urls import include
from rest_framework.authtoken import views

api_urlpatterns = [
    url(r"^api/api-auth/", views.obtain_auth_token, name="obtain-auth-token"),
    url(
        r"^api/sladreboks/",
        include("chemie.shitbox.api.urls", namespace="shitbox-api"),
    ),
]
