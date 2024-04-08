from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path("adminord/", views.adminWord, name ="adminword" ),
    path("form/", views.createWord, name ="innsending" ),
    path("<int:pk>/",views.details, name = "details"  ), 
    path("kategori/", views.category, name = "category"),
    path("adminkategori/", views.admincategoryViews, name="admincategory" ),
    path("redigerkategori/<int:pk>",views.editcategoryViews, name = "editcategory" ),
    path("lagkategori/", views.createcategoryViews, name = "createcategory")
]

