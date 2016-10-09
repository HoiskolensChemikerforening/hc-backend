from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>[0-9]+)/$', views.index),
    url(r'^sok/$', views.search_user, name='sok'),

]
