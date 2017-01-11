from django.conf.urls import url

from .views import index, contact, calendar

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^kontakt/', contact, name="kontakt"),
    url(r'^kalender/', calendar, name="calendar")
]
