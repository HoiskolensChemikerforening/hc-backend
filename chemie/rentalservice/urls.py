from . import views
from django.urls import path

app_name = "rentalservice"

urlpatterns = [
    path("AC/", views.index, name="index_ac"),
    path("promo/", views.index_promo, name="index_promo"),
    path("sportskom/", views.index_sportskom, name="index_sportskom"),
    path("ny_ac/", views.new_object_ac, name="new_object_ac"),
    path("ny_sport/", views.new_object_sport, name="new_object_sport"),
    path("s/<int:rentalobject_id>/", views.detail, name="detail"), 
    path("a/<int:rentalobject_id>/", views.detail_ac, name="detail_ac"), 
    path(
        "a/<int:rentalobject_id>/slett/",
        views.delete_rentalobject_ac,
        name="delete_rentalobject_ac",
    ),
    path(
        "s/<int:rentalobject_id>/slett/",
        views.delete_rentalobject_sportskom,
        name="delete_rentalobject_sportskom",
    ),
    path(
        "a/<int:rentalobject_id>/rediger/",
        views.edit_rentalobject_ac,
        name="edit_rentalobject_ac",
    ),
    path(
        "s/<int:rentalobject_id>/rediger/",
        views.edit_rentalobject_sportskom,
        name="edit_rentalobject_sportskom",
    ),
    path("nyFaktura/", views.new_invoice, name="new_invoice"),
    path("kontaktac/", views.contact_page, name="contact_info"),
    path("kontaktpromo/", views.contact_page_promo, name="contact_info_promo"),
    path(
        "kontaktsportskom/",
        views.contact_page_sportskom,
        name="contact_info_sportskom",
    ),
]
