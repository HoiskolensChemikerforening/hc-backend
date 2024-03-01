from django.urls import path
from . import views


app_name = "wordlist"


urlpatterns = [
    path("", views.ordListe, name="index"),
    path("form/", views.CreateWord, name ="innsending" ),
    path("adminord/", views.adminWord, name ="adminword" ),
    ]
