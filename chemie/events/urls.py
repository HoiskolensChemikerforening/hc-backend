from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required


from . import views

# Events
urlpatterns = [
    url(r'^$', views.ListEventsView.as_view(), name='index'),
    url(r'^past', views.ListPastEventsView.as_view(), name='past'),
    url(r'^create', permission_required('events.add_event')(views.CreateEventView.as_view()), name='create'),
    url(r'^(?P<pk>[0-9]+)', views.ViewEventDetailsView.as_view(), name='detail'),
    url(r'^register/(?P<pk>[0-9]+)', login_required(views.BaseRegisterUserView.as_view()), name='register'),
    url(r'^adminlist/(?P<pk>[0-9]+)', views.view_admin_panel, name='adminlist'),
    url(r'^adminlist/paymentstatus/(?P<registration_id>[0-9]+)', views.change_payment_status, name='payment_status'),
    url(r'^delete/(?P<pk>[0-9]+)', permission_required('events.delete_event')(views.DeleteEventView.as_view()), name='event_id'),
    url(r'^delete/', permission_required('events.delete_event')(views.ListWithDeleteView.as_view()), name='delete'),
]

# Bedpres
urlpatterns += [
    url(r'^bedpres/$', views.ListEventsView.as_view(event_or_bedpres='bedpres'), name='index_bedpres'),
    url(r'^bedpres/past', views.ListPastEventsView.as_view(event_or_bedpres='bedpres'), name='past_bedpres'),
    url(r'^bedpres/create', permission_required('events.add_bedpres')(views.CreateBedpresView.as_view()), name='create_bedpres'),
    url(r'^bedpres/(?P<pk>[0-9]+)', views.ViewEventDetailsView.as_view(event_or_bedpres='bedpres'), name='detail_bedpres'),
    url(r'^bedpres/register/(?P<pk>[0-9]+)', views.register_user_bedpres, name='register_bedpres'),
    url(r'^bedpres/delete/(?P<pk>[0-9]+)', permission_required('events.delete_bedpres')(views.DeleteBedpresView.as_view()), name='event_id_bedpres'),
    url(r'^bedpres/delete', views.ListWithDeleteView.as_view(event_or_bedpres='bedpres'), name='delete_bedpres'),

]