from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send/', views.submit_picture, name="submit"),
    url(r'^$', views.view_carousel, name='display'),
    url(r'^overview/$', views.approve_pictures, name="overview"),
    url(r'^overview/approve/(?P<picture_id>[0-9]+)', views.approve_deny, name="approve"),
    url(r'^overview/deny/(?P<picture_id>[0-9]+)', views.approve_deny, {'deny': True}, name="deny"),
]
