from django.conf.urls import url
from .views import edit_notifications, save_device

app_name = 'notifications'

urlpatterns = [
    url(r'edit/$', edit_notifications, name='edit'),
    url(r'save/$',save_device, name='save')
]