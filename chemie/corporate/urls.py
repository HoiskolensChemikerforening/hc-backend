from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = "corporate"

urlpatterns = [
    url(r"^$",
        views.index,
        name="index"),
    path("interview/", views.interview, name = "interview index"),
    path("company/create/", views.create_company, name="create_company"),
]
