from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.list_all, name="index"),
    path("api/", views.ListAllArticles.as_view()),
    path("api/<int:pk>/", views.NewsDetail.as_view()),
    path("<int:article_id>/<slug:slug>/", views.news_details, name="detail"),
    path("opprett/", views.create_post, name="create"),
    path(
        "slett/<int:article_id>/<slug:slug>/",
        views.delete_article,
        name="delete_article",
    ),
    path(
        "rediger/<int:article_id>/<slug:slug>/",
        views.edit_article,
        name="edit_article",
    ),
]
