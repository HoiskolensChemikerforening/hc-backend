from django.db import models
from push_notifications.models import APNSDevice, GCMDevice
import datetime

# Create your models here.
HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"


class CoffeeSubmission(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def check_last_submission(cls):
        if cls.objects.count() == 0:
            return True
        last_submission_date =cls.objects.latest('id').date
        delta = datetime.datetime.utcnow()-last_submission_date.replace(tzinfo=None)
        minutes_passed = divmod(delta.total_seconds(),60)
        if minutes_passed[0] > 15:  # 15 minutes delay
            return True
        return False


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


