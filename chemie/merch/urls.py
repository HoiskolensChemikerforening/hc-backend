from django.urls import path

from . import views

app_name="merch"

urlpatterns = [
    path("", views.all_merch, name="index"),
    path("opprett/", views.create_merch, name="create"),
    path("<int:pk>", views.detail, name="detail"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path(
        "category-autocomplete/",
        views.CategoryAutocomplete.as_view(),
        name="category-autocomplete",
    ),
]