from django.conf.urls import url
from . import views


app_name = "shop"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^admin/$", views.admin, name="admin"),
    url(r"^admin/refill-balance", views.refill, name="refill"),
    url(r"^admin/add-item/", views.add_item, name="add-item"),
    url(
        r"^admin/add-item/edit/(?P<pk>[0-9]+)",
        views.edit_item,
        name="edit-item",
    ),
    url(r"^admin/add-category/", views.add_category, name="add-category"),
    url(
        r"^admin/remove-item/(?P<pk>[0-9]+)",
        views.remove_item,
        name="remove-item",
    ),
    url(
        r"^admin/activate-happyhour/",
        views.activate_happyhour,
        name="activate-happyhour",
    ),
]
