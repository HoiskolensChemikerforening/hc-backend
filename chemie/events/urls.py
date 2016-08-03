from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all),
    url(r'^create', views.create_event),
    url(r'^(?P<event_id>[0-9]+)', views.view_event_details, name='detail'),
    url(r'^register/(?P<event_id>[0-9]+)', views.register_user, name='register'),
    url(r'^adminlist/(?P<event_id>[0-9]+)', views.view_admin_panel, name='adminlist'),
]