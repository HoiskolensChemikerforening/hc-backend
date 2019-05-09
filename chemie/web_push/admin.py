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


def delete_inactive_devices(modeladmin, request, queryset):

    unregistered_gcm_devices = queryset.filter(gcm_device=None)
    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """
    # unregistered_apns_devices = unregistered_gcm_devices.exclude(apns_device__isnull=True)
    # unregistered_device = unregistered_gcm_devices.filter(apns_device__isnull=True)
    # unregistered_device.delete()
    # unregistered_apns_devices.delte()
    unregistered_gcm_devices.delete()

    inactive_gcm_devices = queryset.filter(gcm_device__active=False)
    inactive_gcm_devices.delete()

    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """

    # inactive_apns_devices = queryset.filter(apns_device__active=False)
    # inactive_apns_devices.delete()


delete_inactive_devices.short_description = "Slett inactive devices"


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
        if obj.gcm_device is not None:
            return obj.gcm_device.registration_id
        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if obj.apns_device is not None:
        #     return obj.apns_device.registration_id
        return "No device registred"

    def Is_active(cls, obj):
        if obj.gcm_device is not None:
            return obj.gcm_device.active
        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if obj.apns_device is not None:
        #     return obj.apns_device.active
        return "No device registred"


@admin.register(CoffeeSubmission)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("date",)


admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
