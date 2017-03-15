from django.conf.urls import url
from .views import index, contact, calendar, post_funds_form

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^kontakt/', contact, name="kontakt"),
    url(r'^kalender/', calendar, name="calendar"),
    url(r'^funds/', post_funds_form, name="fundsapplication"),
]
