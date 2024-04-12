from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path("adminord/<int:pk>/", views.adminWord, name ="adminword" ),
    path("innsending/", views.createWord, name ="innsending" ),
    path("<int:pk>/",views.details, name = "details"  ),
    path("adminkategori/", views.admincategoryViews, name="admincategory" ),
    path("redigerkategori/<int:pk>",views.editcategoryViews, name = "editcategory" ),
    path("lagkategori/", views.createcategoryViews, name = "createcategory")
]

