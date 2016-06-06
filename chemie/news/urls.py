from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new', views.create_article, name='newnews'),
    url(r'^(?P<slug>[\w-]+)/$', views.display_article, name='blog_detail'),
    #url(r'^(?P<slug>[\w-]+)/edit$', views.edit_article, name='blog_detail'),
    #url(r'^(?P<slug>[\w-]+)/delete$', views.delete_article, name='blog_detail'),
]
