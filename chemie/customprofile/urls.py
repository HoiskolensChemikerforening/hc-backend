from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register$', views.register_user),
    url(r'^edit$', views.edit_profile),
    url(r'^changepassword$', views.change_password)
]
