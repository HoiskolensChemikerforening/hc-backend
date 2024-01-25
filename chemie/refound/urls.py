from . import views
from django.urls import path

app_name = "refound"

urlpatterns = [
    path("", views.index, name="index"),
    path("mine/", views.my_refounds, name="myrefounds"),
    path("admin/<int:id>/", views.manage, name="admin"),
    path("admin/<int:id>/avsla/", views.reject_request, name="reject_request"),
    path("admin/<int:id>/godkjenn/", views.approve_request, name="approve_request"),
    ]