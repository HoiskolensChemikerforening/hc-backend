from django.urls import path

from . import views

app_name = "merch"

urlpatterns = [
    path("", views.all_merch, name="index"),
    path("kategori", views.detail_category, name="categories"),
    path("opprett/", views.create_merch, name="create"),
    path("opprett/kategori", views.create_category, name="create_category"),
    path("<int:pk>", views.detail, name="detail"),
    path("<int:pk>/delete", views.delete, name="delete"),
    path("<int:pk>/rediger", views.edit_merch, name="edit_merch"),
    path("kategori/delete/<int:merchcategory_id>", views.delete_categories, name="delete_category"),
    path("kategori/edit/<int:merchcategory_id>", views.edit_category, name="edit_category"),
    path(
        "category-autocomplete/",
        views.CategoryAutocomplete.as_view(),
        name="category-autocomplete",
    ),
]
