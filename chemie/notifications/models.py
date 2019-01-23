from django.db import models
from push_notifications.models import APNSDevice, GCMDevice

# Create your models here.
HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"


class Device(models.Model):
    gcm_device = models.ForeignKey(GCMDevice, blank=False, related_name="Device", on_delete=models.DO_NOTHING)
    # apns_device = models.ForeignKey(APNSDevice, blank=False, related_name="Device")
    coffee_subscription = models.BooleanField(default=True)
    news_subscription = models.BooleanField(default=True)

    def send_notification(self, title, message):
        self.gcm_device.send_message(message,
                                     extra={
                                         "title": title,
                                         "icon": HC_ICON,
                                     })
    # TODO: custom delete function that deletes all gcm/apns-devices when Device is deleted
