from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = "corporate"

urlpatterns = [
    path("", views.index, name="index"),
    path("intervju/", views.interview, name="interview"),
    path("company/create/", views.create_company, name="create_company"),
    path("company", views.list_companies, name="list_companies"),
    path("intervju/create", views.create_interview, name="create_interview"),
    path("intervju/<int:interview_id>/", views.interview_index, name="interview_index")
]
