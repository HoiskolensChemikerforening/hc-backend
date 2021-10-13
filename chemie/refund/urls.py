from . import views
from django.urls import path

app_name = "refund"

urlpatterns = [
    path("",views.index, name = "index"),
]