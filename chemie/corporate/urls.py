from django.urls import path
from . import views

app_name = "corporate"


urlpatterns = [
    path("", views.ListCompany.as_view()),
    path("<int:pk>/", views.DetailCompany.as_view())
]

"""
urlpatterns = [
    path("", views.index, name="index"),
    path("oversikt/", views.company_list, name="company_list"),
    path("oversikt/<int:pk>/", views.company_detail, name="company_detail"),
    path("overskit/lag/", views.company_create, name="company_create"),
    path("intervju/", views.interview_list, name="interview_list"),
    path("intervju/lag", views.interview_create, name="interview_create"),
    path("intervju/<int:interview_id>/", views.interview_detail, name="interview_detail")
]
"""
