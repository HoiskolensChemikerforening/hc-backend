from . import views
from django.urls import path

app_name = "stock"

urlpatterns = [
    path("", views.index, name = "index"),
    path("admin/", views.stockadmin, name = "admin"),
    path("admin/<int:id>", views.individual, name = "individual"),
]