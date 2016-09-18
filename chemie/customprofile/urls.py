from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register$', views.register_user, name='register'),
    url(r'^edit$', views.edit_profile, name='edit'),
    url(r'^changepassword$', views.change_password, name='changepassword'),
    url(r'^forgotpassword', views.forgot_password, name='forgotpassword'),
    url(r'^aktiver/(?P<code>[a-z0-9]{32})/?', views.activate_password, name='activate'),
]
