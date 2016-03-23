from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.view_lockers, name='index'),
]
