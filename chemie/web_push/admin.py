from django.contrib import admin, messages
from .models import Device, CoffeeSubmission
from push_notifications.models import (
    APNSDevice,
    GCMDevice,
    WebPushDevice,
    WNSDevice,
)
from push_notifications.admin import GCMDeviceAdmin
from push_notifications.gcm import GCMError


@admin.register(Device)
class WebPushDeviceAdmin(admin.ModelAdmin):
    list_display = ("owner", "date_created", "is_active", "Device_token")
    actions = ["send_message"]

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

    def send_messages(self, request, queryset):
        """
        Provides error handling for DeviceAdmin send_message and send_bulk_message methods.
        """
        ret = []
        errors = []
        r = ""

        for device in queryset.exclude(gcm_device=None):
            try:
                r = device.gcm_device.send_message("Test single notification")
                if r:
                    ret.append(r)

            except GCMError as e:
                errors.append(str(e))

        # Because NotRegistered and InvalidRegistration do not throw GCMError
        # catch them here to display error msg.

        for r in ret:
            if "error" in r["results"][0]:
                errors.append(r["results"][0]["error"])
        if errors:
            self.message_user(
                request,
                "Some messages could not be processed: %r"
                % (", ".join(errors)),
                level=messages.ERROR,
            )
        if ret:
            if len(errors) == len(ret):
                return
            if errors:
                msg = "Some messages were sent: %s" % (ret)
            else:
                msg = "All messages were sent: %s" % (ret)
            self.message_user(request, msg)

    def send_message(self, request, queryset):
        self.send_messages(request, queryset)


@admin.register(CoffeeSubmission)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("date",)


admin.site.unregister(WNSDevice)
admin.site.unregister(WebPushDevice)
admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
