from . import views
from django.urls import path

app_name = "rentalservice"

urlpatterns = [
    path("", views.index, name="index"),
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
    path("<int:rentalobject_id>/kontakt/", views.contact, name="contact"),
    path("nyFaktura/", views.new_invoice, name="new_invoice"),
]
