from django.conf.urls import url

from . import views, models

urlpatterns = [
    url(r'^$', views.view_lockers, name='index'),
    url(r'^group=(?P<page>[0-9]+)$', views.view_lockers, name='index'),
    url(r'^registrer/(?P<number>[0-9]+)/$', views.register_locker, name='register'),
    url(r'^aktiver/(?P<code>[a-z0-9]{32})/?', views.activate_ownership, name='activate')
]
