from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register_user),
    url(r'^login/', views.user_login),
]
