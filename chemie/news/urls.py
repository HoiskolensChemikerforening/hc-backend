from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all),
    url(r'^detail/(?P<article_id>[0-9]+)/[\w0-9/]+', views.news_details),
    url(r'^create', views.create_post),
]