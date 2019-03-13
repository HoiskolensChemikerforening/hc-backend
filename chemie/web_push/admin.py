from django.contrib import admin
from .models import Device,CoffeeSubmission
from django.contrib import admin
from push_notifications.models import APNSDevice, GCMDevice, WebPushDevice, WNSDevice
from push_notifications.admin import DeviceAdmin, GCMDeviceAdmin


# TODO fix deletion of device and gcm device
# TODO style admin page
# TODO remove gcm_device/apns_device from admin page
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('gcm_device','coffee_subscription', 'news_subscription','date_created')

@admin.register(CoffeeSubmission)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('date',)

admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
