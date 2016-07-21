from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list),
    url(r'^create', views.register_event),
]