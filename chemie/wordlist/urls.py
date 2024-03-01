from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path("form/", views.CreateWord, name ="innsending" ),
    path("adminkategori/", views.categoryViews, name="admincategory" )
]
