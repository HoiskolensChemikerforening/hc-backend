from django.conf.urls import url

from . import views, models

urlpatterns = [
    url(r'^$', views.view_lockers, name='index'),
    url(r'^registrere-skap/(?P<number>[0-9]+)/$', views.register_locker,
    name = 'register'),
]
