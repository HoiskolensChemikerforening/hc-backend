from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path("adminord/<int:pk>/", views.adminWord, name ="adminword" ),
    path("innsending/", views.createWord, name ="innsending" ),
    path("<int:pk>/",views.details, name = "details"  ), 
    path("kategori/", views.category, name = "category"),
    path("adminkategori/", views.categoryViews, name="admincategory" ),
]

