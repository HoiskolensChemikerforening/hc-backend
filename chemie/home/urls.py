from django.conf.urls import url
from .views import index, contact, calendar, request_funds

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^kontakt/', contact, name="kontakt"),
    url(r'^kalender/', calendar, name="calendar"),
    url(r'^funds/', request_funds, name="fundsapplication"),
]
