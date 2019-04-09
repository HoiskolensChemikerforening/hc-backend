from django.urls import path
from . import views

app_name = "corporate"

urlpatterns = [
    path("", views.index, name="index"),
    path("intervju/", views.interview_list, name="interview_list"),
    path("company/", views.company_list, name="company_list"),
    path("company/<int:pk>/", views.company_detail, name="company_detail"),
    path("company/create/", views.company_create, name="company_create"),
    path("intervju/create", views.interview_create, name="interview_create"),
    path("intervju/<int:interview_id>/", views.interview_detail, name="interview_detail")
]
