from django.urls import path

from . import views, views_admin

app_name = "cgp"


urlpatterns = [
    path(
        "", views.index, name="index"
    ),
    path(
        "admin/", views_admin.cgp_admin, name="cgp_admin"
    ),
    path(
        "<slug:slug>/", views.vote_index, name="vote_index"
    ),
    #path("admin/<id:id>/", views_admin.cgp_edit, name="cgp_edit"),
    path("api", views.CGPListViewTemplate.as_view(), name="cgpapi")
    ]