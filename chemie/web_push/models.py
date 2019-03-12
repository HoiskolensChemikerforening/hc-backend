from django.db import models
from push_notifications.models import APNSDevice, GCMDevice
import datetime
from django.db.models.signals import pre_delete


HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"


class CoffeeSubmission(models.Model):
    """ Submission thats created each time a notification is send """
    date = models.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def check_last_submission(cls):
        """ Make sure that the send_notification is not activated too frequently """
        if cls.objects.count() == 0:
            return True
        last_submission_date =cls.objects.latest('id').date
        delta = datetime.datetime.utcnow()-last_submission_date.replace(tzinfo=None)
        minutes_passed = divmod(delta.total_seconds(),60)
        if minutes_passed[0] > 15:  # 15 minutes delay
            return True
        return False


class Device(models.Model):
    """ Overall model which saves gcm/apns device and the users subsciption settings """
    gcm_device = models.ForeignKey(GCMDevice, related_name="Device", on_delete=models.DO_NOTHING)
    # apns_device = models.ForeignKey(APNSDevice, blank=False, related_name="Device")
    coffee_subscription = models.BooleanField(default=True)
    news_subscription = models.BooleanField(default=True)

    def send_notification(self, title, message):
        """" Send notification to gcm_device """
        self.gcm_device.send_message(message,
                                     extra={
                                         "title": title,
                                         "icon": HC_ICON,
                                     })


def delete_device_signal(sender, instance, **kwargs):
    """ Deletes gcm_device when deleting Device """
    instance.gcm_device.delete()

# Connects delete_device_signal with the pre_delete signal reciever
pre_delete.connect(delete_device_signal, sender=Device)


