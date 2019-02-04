from django.conf.urls import url

from . import views

app_name = "news"

urlpatterns = [
    url(r"^$", views.list_all, name="index"),
    url(
        r"^detail/(?P<article_id>[0-9]+)/(?P<slug>[\w0-9/]+)",
        views.news_details,
        name="detail",
    ),
    url(r"^create", views.create_post, name="create"),
    url(
        r"^delete/(?P<article_id>[0-9]+)/(?P<slug>[\w0-9/]+)",
        views.delete_article,
        name="delete_article",
    ),
    url(
        r"^edit/(?P<article_id>[0-9]+)/(?P<slug>[\w0-9/]+)",
        views.edit_article,
        name="edit_article",
    ),
]
