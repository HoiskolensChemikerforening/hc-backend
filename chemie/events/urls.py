from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all, name='index'),
    url(r'^create', views.create_event, name='create'),
    url(r'^(?P<event_id>[0-9]+)', views.view_event_details, name='detail'),
    url(r'^register/(?P<event_id>[0-9]+)', views.register_user, name='register'),
    url(r'^adminlist/(?P<event_id>[0-9]+)', views.view_admin_panel, name='adminlist'),
    url(r'^adminlist/paymentstatus/(?P<registration_id>[0-9]+)', views.change_payment_status, name='payment_status'),
    url(r'^delete/(?P<event_id>[0-9]+)', views.delete_event, name='event_id'),
    url(r'^delete/', views.list_with_delete, name='delete'),

]
