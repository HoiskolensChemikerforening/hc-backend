from . import views
from django.urls import path

app_name = "rentalservice"

urlpatterns = [
    path("AC", views.index, name="index"),
    path("promo", views.index_promo, name="index_promo"),
    path("sportskom", views.index_sportskom, name="index_sportskom"),
    path("ny/", views.new_object, name="new_object"),
    path("<int:rentalobject_id>/", views.detail, name="detail"),
    path(
        "<int:rentalobject_id>/slett/",
        views.delete_rentalobject,
        name="delete_rentalobject",
    ),
    path(
        "<int:rentalobject_id>/rediger/",
        views.edit_rentalobject,
        name="edit_rentalobject",
    ),
    path("nyFaktura/", views.new_invoice, name="new_invoice"),
    path("kontaktac/", views.contact_page, name="contact_info"),
    path("kontaktpromo/", views.contact_page_promo, name="contact_info_promo"),
    path("kontaktsportskom/", views.contact_page_sportskom, name="contact_info_sportskom"),
]
