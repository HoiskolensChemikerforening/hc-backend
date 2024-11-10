from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path(
        "adminword/<int:pk>/<int:klassetall>/",
        views.adminWord,
        name="adminword",
    ),
    path("innsending/", views.createWord, name="innsending"),
    path("<int:pk>/<int:klassetall>/", views.details, name="details"),
    path(
        "<int:pk>/<int:klassetall>/delete/", views.word_delete, name="delete"
    ),
    path(
        "<int:pk>/slettkategori/",
        views.deletecategoryViews,
        name="deletecategory",
    ),
    path("adminkategori/", views.admincategoryViews, name="admincategory"),
    path(
        "redigerkategori/<int:pk>",
        views.editcategoryViews,
        name="editcategory",
    ),
    path("lagkategori/", views.createcategoryViews, name="createcategory"),
]
