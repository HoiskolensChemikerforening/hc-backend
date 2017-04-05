from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send/', views.post_pic, name="submit"),
    url(r'^$', views.view_carousel, name='display'),
    url(r'^approve/$', views.view_pic_approve, name="overview"),
    url(r'^approve/(?P<picture_id>[0-9]+)', views.approve, name="approvepic"),
]
