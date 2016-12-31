from django.conf.urls import url

from .views import index, contact

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^kontakt/', contact, name="kontakt"),
]
