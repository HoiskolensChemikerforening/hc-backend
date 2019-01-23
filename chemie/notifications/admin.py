from django.contrib import admin
from .models import Device
from django.contrib import admin
from push_notifications.models import APNSDevice, GCMDevice


@admin.register(Device)
class EventAdmin(admin.ModelAdmin):
    list_display = ('gcm_device', 'coffee_subscription', 'news_subscription')

