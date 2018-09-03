from django.conf.urls import url
from .views import index, refill


app_name = 'shop'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^refill-balance', refill, name='refill')
]