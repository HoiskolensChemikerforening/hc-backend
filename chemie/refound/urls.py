from . import views
from django.urls import path

app_name = "refound"

urlpatterns = [
    path("", views.index, name="index"),
    path("mine/", views.my_refounds, name="myrefounds"),
    path("detalj/<int:id>/", views.detail_view, name="detail"),
    path("admin/", views.admin_refounds, name="admin_refounds"),
    path("admin/<int:id>/avsla/", views.reject_request, name="reject_request"),
    path(
        "admin/<int:id>/godkjenn/",
        views.approve_request,
        name="approve_request",
    ),
    path(
        "admin/<int:id>/nullstill/", views.reset_status, name="reset_request"
    ),
    path(
        "admin/oversikt/<int:year>/",
        views.annual_account_detail,
        name="annual_account",
    ),
    path(
        "admin/detalj/<int:id>/", views.detail_admin_view, name="admin_detail"
    ),
    path(
        "admin/oversikt/<int:year>/delete/",
        views.delete_annual_report,
        name="delete_annual_account",
    ),
]
