from django.urls import path

from . import views, views_admin

app_name = "cgp"


urlpatterns = [
    path("", views.index, name="list_all"),
    path(
        "admin/", views_admin.admin_start_cgp, name="admin_start_cgp"
    ),
    ]