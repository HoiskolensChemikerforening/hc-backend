from django.urls import path

from . import views, views_admin

app_name = "cgp"


urlpatterns = [
    path("", views.index, name="index"),
    path(
        "admin/", views_admin.admin_start_cgp, name="admin_start_cgp"
    ),
    path(
        "<slug:slug>/", views.vote_index, name="vote_index"
    ),
    path("api", views.CGPListViewTemplate.as_view(), name="cgpapi")
    ]