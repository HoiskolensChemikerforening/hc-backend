from django.conf.urls import url
from .views import index


app_name = 'shop'

urlpatterns = [
    url(r'^$', index, name='index'),
]