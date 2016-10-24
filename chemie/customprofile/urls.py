from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register$', views.register_user, name='register'),
    url(r'^edit$', views.edit_profile, name='edit'),
    url(r'^forgotpassword', views.forgot_password, name='forgotpassword'),
    url(r'^aktiver/(?P<code>[a-z0-9]{32})/?', views.activate_password, name='activate'),
    url(r'^medlemmer/endre/(?P<profile_id>[0-9]+)', views.change_membership_status, name='membership'),
    url(r'^medlemmer', views.view_memberships, name='memberships'),
]
