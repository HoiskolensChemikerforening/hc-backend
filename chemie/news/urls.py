from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all, name = 'index'),
    url(r'^detail/(?P<article_id>[0-9]+)/(?P<slug>[\w0-9/]+)', views.news_details, name='detail'),
    url(r'^create', views.create_post, name = 'create')
]