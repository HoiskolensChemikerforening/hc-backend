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
        "admin/<int:cgp_id>/", views_admin.cgp_edit, name="cgp_edit"
    ),
    path("admin/<int:cgp_id>/group/add/", views_admin.group_add, name="group_add"),
    path("admin/<int:cgp_id>/group/<int:group_id>/", views_admin.group_edit, name="group_edit"),
    path("admin/country/add/", views_admin.country_add, name="country_add"),
    path("admin/country/<int:country_id>/", views_admin.country_edit, name="country_edit"),
    path(
        "<slug:slug>/", views.vote_index, name="vote_index"
    ),
    #path("admin/<id:id>/", views_admin.cgp_edit, name="cgp_edit"),
    path("api", views.CGPListViewTemplate.as_view(), name="cgpapi")
    ]