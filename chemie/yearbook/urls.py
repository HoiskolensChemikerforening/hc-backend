from django.conf.urls import url

from . import views, models

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>[0-9]+)/$', views.get_images),

]
