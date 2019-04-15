from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("mine-kvitteringer", views.view_my_receipts, name="receipts"),
    path("admin/", views.admin, name="admin"),
    path("admin/fyll-konto", views.refill, name="refill"),
    path("admin/opprett-vare/", views.add_item, name="add-item"),
    path(
        "admin/opprett-vare/endre/<int:pk>)",
        views.edit_item,
        name="edit-item",
    ),
    path("admin/opprett-kategori/", views.add_category, name="add-category"),
    path(
        "admin/fjern-vare/<int:pk>)",
        views.remove_item,
        name="remove-item",
    ),
    path(
        "admin/aktiver-happyhour/",
        views.activate_happyhour,
        name="activate-happyhour",
    ),
]
