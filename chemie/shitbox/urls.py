from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_name, name = 'get_name'),
    url(r'^thanks', views.thank_you, name = 'thank_you')
]
