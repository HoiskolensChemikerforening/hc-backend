from . import views
from django.urls import path

app_name = "stock"

urlpatterns = [
    path("", views.index, name = "stock")
]