from django.conf.urls import url
from .views import index, contact, calendar, request_funds, edit_flatpage, request_office #importert

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^contact/', contact, name="kontakt"),
    url(r'^calendar/', calendar, name="calendar"),
    url(r'^funds/', request_funds, name="fundsapplication"),
    url(r'^office-access/', request_office, name='officeaccess'),
    url(r'^flatpage/(?P<url>.*)$', edit_flatpage, name='edit_flatpage'),
]
