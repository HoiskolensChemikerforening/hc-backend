from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.view_lockers, name='index'),
    url(r'^(?P<page>[0-9]+)$', views.view_lockers, name='detail'),
    url(r'^registrer/(?P<number>[0-9]+)/$', views.register_locker, name='registrer'),
    url(r'^aktiver/(?P<code>[a-z0-9]{32})/?', views.activate_ownership, name='activate'),
    url(r'^administrer', views.manage_lockers, name='administrate'),
]
