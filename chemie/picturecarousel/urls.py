from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send/', views.post_pic, name="create"),
    url(r'^$', views.view_carousel, name='view'),
    url(r'^approve/$', views.view_pic_approve, name="approve"),
    url(r'^approve/(?P<picture_id>[0-9]+)', views.approve, name="approvepic"),
]
