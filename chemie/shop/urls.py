from django.urls import path

from . import views

app_name = "shop"

shop_url_patterns = [
    path("", views.index, name="index"),
    path("mine-kvitteringer", views.view_my_receipts, name="receipts"),
    path("mine-paafyll", views.view_my_refills, name="refills"),
    path("statistikk", views.view_statistics, name="statistics"),
    path("fjern-handlekurv/", views.remove_cart, name="remove-cart"),
    path(
        "item-autocomplete/",
        views.ItemAutocomplete.as_view(),
        name="item-autocomplete",
    ),
]

admin_shop_urlpatterns = [
    path("admin/", views.admin, name="admin"),
    path("admin/opprett-kategori/", views.add_category, name="add-category"),
    path("admin/opprett-vare/", views.add_item, name="add-item"),
    path(
        "admin/opprett-vare/endre/<int:pk>", views.edit_item, name="edit-item"
    ),
    path("admin/fyll-konto", views.refill, name="refill"),
    path("fjern-vare/<int:pk>", views.remove_item, name="remove-item"),
    path(
        "admin/aktiver-happyhour/",
        views.activate_happyhour,
        name="activate-happyhour",
    ),
    path(
        "admin/alle-kvitteringer", views.view_all_receipts, name="all_receipts"
    ),
    path("admin/alle-paafyll", views.view_all_refills, name="all_refills"),
    path(
        "admin/monthly_statistics",
        views.view_monthly_statistics,
        name="monthly_statistics",
    ),
]

urlpatterns = shop_url_patterns + admin_shop_urlpatterns
