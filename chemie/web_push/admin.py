from django.contrib import admin
from .models import Device, CoffeeSubmission
from django.contrib import admin
from push_notifications.models import (
    APNSDevice,
    GCMDevice,
    WebPushDevice,
    WNSDevice,
)
from push_notifications.admin import DeviceAdmin, GCMDeviceAdmin


# TODO fix deletion of device and gcm device
# TODO style admin page
# TODO remove gcm_device/apns_device from admin page


def delete_inactive_devices(modeladmin, request, queryset):
    inactive_gcm_devices = queryset.filter(gcm_device__active=False)
    inactive_gcm_devices.delete()

    # inactive_apns_devices = queryset.filter(apns_device__active=False)
    # inactive_apns_devices.delete()


delete_inactive_devices.short_description = "Delete inactive devices"


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "coffee_subscription",
        "date_created",
        "is_active",
        "Device_token",
    )
    actions = [delete_inactive_devices]

    def Device_token(cls, obj):
        return obj.gcm_device.registration_id

    def Is_active(cls, obj):
        return obj.gcm_device.active


@admin.register(CoffeeSubmission)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("date",)


admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
