from django.db import models
from extended_choices import Choices
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from push_notifications.models import APNSDevice, GCMDevice
import datetime
import pytz

HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"

SUSBSCRIPTION_CHOICES = Choices(
    ("COFFEE", 1, "Coffee"),
    ("NEWS", 2, "News"),
    ("HAPPY", 3, "Happy"),
)


class CoffeeSubmission(models.Model):
    """ Submission that's created each time a notification is send """

    date = models.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def fifteen_minutes_has_passed(cls):
        """ Make sure that the send_notification is not activated too frequently """
        if cls.objects.count() == 0:
            return True

        # Checks if fifteen minutes have passed since last CoffeSubmission object was created
        fifteen_minutes = datetime.timedelta(0, 900)
        now = datetime.datetime.now()
        last_coffee_submission_date = (now - fifteen_minutes).replace(tzinfo=pytz.timezone('Europe/Oslo'))

        if CoffeeSubmission.objects.filter(
            date__gte=last_coffee_submission_date
        ).exists():
            return False
        return True

    @classmethod
    def get_latest_submission(cls):
        try:
            coffee = cls.objects.latest("date")
        except ObjectDoesNotExist:
            coffee = None
        return coffee

    @staticmethod
    def send_coffee_notification(subscribers):
        for subscriber in subscribers:
            devices = subscriber.profile.devices.all()

            time_mark = datetime.datetime.now().time()
            hour_mark = str(time_mark.hour)
            minute_mark = int(time_mark.minute)
            if int(minute_mark) < 10:
                minute_mark = "0" + str(minute_mark)
            coffee_message = "Laget klokken: " + hour_mark + ":" + str(minute_mark)
            [
                device.send_notification(
                    "Kaffe på kontoret", coffee_message
                )
                for device in devices
            ] # one-liner for loop


class Device(models.Model):
    """ Overall model which saves gcm/apns device and the users subsciption settings """

    owner = models.ForeignKey(
        User, verbose_name="eier", on_delete=models.CASCADE
    )
    gcm_device = models.ForeignKey(
        GCMDevice,
        blank=True,
        null=True,
        related_name="Device",
        on_delete=models.DO_NOTHING,
        verbose_name="Tredje parts api for android telefoner",
    )
    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """
    # apns_device = models.ForeignKey(
    #   APNSDevice,
    #   blank=True,
    #   null=True,
    #   related_name="Device",
    #   on_delete=models.DO_NOTHING,
    #   verbose_name="Tredje parts api for apple telefoner"
    # )

    date_created = models.DateTimeField(auto_now_add=True)

    def send_notification(self, title, message):
        """" Send notification to gcm_device """
        if self.gcm_device is not None:
            self.gcm_device.send_message(
                message, extra={"title": title, "icon": HC_ICON}
            )

        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if self.apns_device is not None:
        #     self.apns_device.send_message(
        #         message, extra={"title": title, "icon": HC_ICON}
        #     )

    @property
    def is_active(self):
        if self.gcm_device is not None:
            return self.gcm_device.active

        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if self.apns_device is not None:
        #     return self.apns_device.active

    @classmethod
    def add_device(cls, device_type, token, user):
        status = 301
        if device_type=="FCM":
            registered_device = GCMDevice.objects.filter(
                registration_id=token
            )
            if registered_device.count() == 0:
                gcm_device = GCMDevice.objects.create(
                    registration_id=token,
                    cloud_message_type="FCM",
                    user=user,
                    #apns_device=None
                )
                device = cls.objects.create(
                    gcm_device=gcm_device, owner=user
                )
                user.profile.devices.add(device)
                status = 201

        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # elif device_type=="APNS":
        #     registered_device = APNSDevice.objects.filter(
        #         registration_id=token
        #     )
        #     if registered_device.count() == 0:
        #         apns_device = APNSDevice.objects.create(
        #             registration_id=token,
        #             user=user,
        #         )
        #         device = cls.objects.create(
        #             apns_device=apns_device,
        #             owner=user,
        #             gcm_device=None
        #         )
        #         user.profile.devices.add(device)
        #         status = 201

        if user.profile.subscriptions.count() < len(SUSBSCRIPTION_CHOICES):
            for sub_type in SUSBSCRIPTION_CHOICES:
                if user.profile.subscriptions.filter(subscription_type=sub_type[0]).count() == 0:
                    sub = Subscription.objects.create(
                        subscription_type=sub_type[0],
                        owner=user
                        )
                    user.profile.subscriptions.add(sub)
            user.profile.save()

        if cls.objects.filter(owner=user).count() > 5:
            cls.objects.latest("-date_created").delete()
        return status

    @classmethod
    def delete_inactive_gcm_device(cls):
        count = GCMDevice.objects.count()
        unregistered_gcm_devices = Device.objects.filter(gcm_device=None)
        unregistered_gcm_devices.delete()

        inactive_gcm_devices = Device.objects.filter(gcm_device__active=False)
        inactive_gcm_devices.delete()
        return count - GCMDevice.objects.count()


def delete_device_signal(sender, instance, **kwargs):
    """ Deletes gcm_device when deleting Device """
    if instance.gcm_device is not None:
        instance.gcm_device.delete()
    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """
    # if instance.apns_device is not None:
    #     instance.apns_device.delete()


# Connects delete_device_signal with the pre_delete signal reciever
pre_delete.connect(delete_device_signal, sender=Device)


class Subscription(models.Model):
    active = models.BooleanField(default=True)

    subscription_type = models.PositiveSmallIntegerField(choices=SUSBSCRIPTION_CHOICES)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Eier av abonomentet")

    def __str__(self):
        sub_type = SUSBSCRIPTION_CHOICES[self.subscription_type-1][-1]
        sub_type += ": {}".format(str(self.active))
        return sub_type