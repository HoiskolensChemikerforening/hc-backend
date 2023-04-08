from django.urls import path

from . import views, views_admin
from .models import Country, Group


app_name = "cgp"


urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", views_admin.cgp_admin, name="cgp_admin"),
    path("admin/<int:cgp_id>/", views_admin.cgp_edit, name="cgp_edit"),
    path("admin/<int:cgp_id>/group/add/", views_admin.group_add, name="group_add"),
    path("admin/<int:cgp_id>/group/<int:group_id>/", views_admin.group_edit, name="group_edit"),
    path("admin/<int:cgp_id>/group/<int:group_id>/delete/", views_admin.DeleteView.as_view(
            key="group_id", objecttype=Group, redirect_url="cgp_edit"), name="group_delete"
        ),
    path("admin/country/add/", views_admin.country_add, name="country_add"),
    path("admin/country/<int:country_id>/", views_admin.country_edit, name="country_edit"),
    path("admin/country/<int:country_id>/delete/", views_admin.DeleteView.as_view(
        key="country_id", objecttype=Country, redirect_url="cgp_admin"), name="country_delete"
         ),
    path("<slug:slug>/", views.vote_index, name="vote_index"),
    path("api/votes/", views.CGPListViewTemplate.as_view(), name="cgpapi"),
    path("api/groups/", views.GroupsListViewTemplate.as_view(), name="cgpapigroups"),
    ]