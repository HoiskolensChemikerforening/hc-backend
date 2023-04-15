from django.urls import path

from . import api_views as views


social_api_urlpatterns = [
    path("api/social/", views.SocialListCreate.as_view()),
    path("api/social/kommende/", views.SocialUpcoming.as_view()),
    path("api/social/mine/", views.MySocial.as_view()),
]

bedpres_api_urlpatterns = [
    path("api/bedpres/", views.BedpresListCreate.as_view()),
    path("api/bedpres/kommende/", views.BedpresUpcoming.as_view()),
    path("api/bedpres/mine/", views.MyBedpres.as_view()),
]

api_urlpatterns = social_api_urlpatterns + bedpres_api_urlpatterns
