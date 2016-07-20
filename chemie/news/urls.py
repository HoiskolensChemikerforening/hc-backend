from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new', views.create_article, name='newnews'),
    url(r'(?P<pk>[0-9]+)/$', views.display_article, name='blog_detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.edit_article, name='blog_detail'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.delete_article, name='blog_detail'),
]
